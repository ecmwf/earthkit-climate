import geopandas as gpd
import xarray as xr
import numpy as np

import typing as T

from earthkit.climate.tools import get_how, get_dim_key, get_spatial_dims, WEIGHTS_DICT, nanaverage
from earthkit.climate import aggregate


def transform_from_latlon(lat, lon):
    """
    Return an Affine transformation of input 1D arrays of lat / lon.
    This assumes that both lat and lon are regular and contiguous.
    """
    from affine import Affine

    trans = Affine.translation(lon[0] - (lon[1] - lon[0])/2, lat[0] - (lat[1] - lat[0])/2)
    scale = Affine.scale(lon[1] - lon[0], lat[1] - lat[0])

    return trans * scale

def rasterize(
    shape_list: T.List,
    coords: xr.core.coordinates.Coordinates,
    lat_key: str = 'latitude',
    lon_key: str = 'longitude',
    dtype: type = int,
    **kwargs
):
    """Rasterize a list of geometries onto the given xarray coordinates.
    This only works for regular and contiguous latitude and longitude grids.

    Parameters
    ----------
    shape_list (affine.Affine): List of geometries
    coords (xarray.coords): Coordinates of dataarray to be masked

    lat_key/lon_key: name of the latitude/longitude variables in the coordinates object

    fill: value to fill points which are not within the shape_list, default is 0
    dtype: datatype of the returned mask, default is `int`

    kwargs: Any other kwargs accepted by rasterio.features.rasterize

    Returns
    -------
    xr.DataArray mask where points not inside the shape_list are set to `fill` value


    """
    from rasterio import features

    transform = transform_from_latlon(coords[lat_key], coords[lon_key])
    out_shape = (len(coords[lat_key]), len(coords[lon_key]))
    raster = features.rasterize(
        shape_list, out_shape=out_shape,
        transform=transform,
        dtype=dtype, **kwargs
    )
    spatial_coords = {lat_key: coords[lat_key], lon_key: coords[lon_key]}
    return xr.DataArray(raster, coords=spatial_coords, dims=(lat_key, lon_key))


def mask_contains_points(
        shape_list, coords,
        lat_key='lat', lon_key='lon',
        **kwargs
):
    '''
    Return a mask array for the spatial points of data that
    lie within shapes in shape_list.
    Function uses matplotlib.Path so can accept a list of points,
    this is much faster than shapely.
    It was initially included for use with irregular data but has been
    constructed to also accept regular data and return in the same
    format as the rasterize function.
    '''
    import matplotlib.path as mpltPath

    lat_dims = coords[lat_key].dims
    lon_dims = coords[lon_key].dims
    # Assert that latitude and longitude have the same dimensions
    #   (irregular data, e.g. x,y or obs)
    # or the dimensions are themselves (regular data) but we will probably
    # just use the rasterize function for the regular case
    assert (
        (lat_dims==lon_dims) or
        (lat_dims==(lat_key,) and lon_dims==(lon_key,))
    )
    if (lat_dims==(lat_key,) and lon_dims==(lon_key,)):
        lon_full, lat_full = np.meshgrid(
            coords[lon_key].values,
            coords[lat_key].values,
        )
    else:
        lon_full, lat_full = (
            coords[lon_key].values,
            coords[lat_key].values,
        )
    # convert lat lon pairs to to points:
    points = list(zip(
        lon_full.flat,
        lat_full.flat,
    ))

    # get spatial dims and create output array:
    spatial_dims = list(set(lat_dims+lon_dims))
    outdata_shape = [len(coords[dim]) for dim in spatial_dims]
    outdata = np.zeros(outdata_shape).astype(bool)*np.nan
    # loop over shapes and mask any point that is in the shape
    for shape in shape_list:
        for shp in shape[0]:
            shape_exterior = shp.exterior.coords.xy
            shape_exterior = list(zip(
                list(shape_exterior[0]),   # longitudes
                list(shape_exterior[1]),   # latitudes
            ))
            path = mpltPath.Path(shape_exterior)
            outdata.flat[path.contains_points(points)] = True

    out_coords = {coord: coords[coord] for coord in spatial_dims}
    outarray = xr.DataArray(outdata, coords=out_coords, dims=spatial_dims)

    return outarray


def geopandas_to_shape_list(geodataframe):
    return [row[1]['geometry'] for row in geodataframe.iterrows()]

def _shape_mask_iterator(shapes, target, regular_grid=True, **kwargs):
    """
    Method which iterates over shape mask methods.
    """
    if isinstance(shapes, gpd.GeoDataFrame):
        shapes = geopandas_to_shape_list(shapes)
    if regular_grid:
        mask_function = rasterize
    else:
        mask_function = mask_contains_points
    for shape in shapes:
        shape_da = mask_function(
            [shape], target.coords,
            **kwargs
        )
        yield shape_da


def masks(
    dataarray: T.Union[xr.DataArray, xr.Dataset],
    geodataframe: gpd.GeoDataFrame,
    mask_dim: str = 'FID',
    regular_grid: bool = True,
    **kwargs
):
    """
    Apply multiple shape masks to some gridded data. Each feauture in shape is treated as an individual mask to apply to
    data. NOTE: The data provided is returned with an additional dimension equal in length to the number of features in
    the shape object, this can result in very large files which will slow down your workflow. It may be better to loop
    over individual features, or directly apply the mask with the ct.shapes.average or ct.shapes.reduce functions.

    Args:
        dataarray: An xarray data object, must have geospatial coordinates.
        shape: CDS remote layer/shape/geojson object.
        **kwargs:
            kwargs recognised by rasterio.features.rasterize

    Returns:
        A masked data array with dimensions [feautre_id] + [data.dims].
        Each slice of layer corresponds to a feature in layer.
    """
    masked_arrays = []
    for mask in _shape_mask_iterator(geodataframe, dataarray, **kwargs):
        masked_arrays.append(dataarray.where(mask))
    
    if isinstance(mask_dim, str):
        mask_dim_values = geodataframe.get(mask_dim, np.arange(len(masked_arrays))).to_numpy()
    elif isinstance(mask_dim, dict):
        assert len(mask_dim)==1, 'If provided as a dictionary, mask_dim should have onlly one key value pair'
        mask_dim, mask_dim_values = mask_dim.items()
    else:
        raise ValueError('Unrecognised format for mask_dim, should be a string or length one dictionary')
    
    out = xr.concat(masked_arrays, dim=mask_dim)
    out = out.assign_coords({mask_dim: mask_dim_values})

    out.attrs.update(geodataframe.attrs)

    return out


def reduce(
    dataarray: T.Union[xr.DataArray, xr.Dataset],
    geodataframe: gpd.GeoDataFrame,
    how: T.Union[T.Callable, str] = nanaverage,
    weights: T.Union[None, str, np.ndarray] = None,
    lat_key: T.Union[None, str] = None,
    lon_key: T.Union[None, str] = None,
    mask_dim = 'FID',
    **kwargs
):
    '''
    Apply a shape object to an xarray.DataArray object using the specified 'how' method. Geospatial coordinates
    (lat and lon) are reduced to a dimension representing the list of features in the shape object.

    Args:
        data: Xarray data object (must have geospatial coordinates).
        geodataframe: geopandas dataframe
        how: method used to apply mask. Default='mean', which calls np.nanmean
        weighted: To perform a latitude weighted calculation
                  for regular lat/lon grids. Default=False
        **kwargs:
            kwargs recognised by the how function

    Returns:
        A data array with dimensions [features] + [data.dims not in ['lat','lon']].
        Each slice of layer corresponds to a feature in layer.

    '''

    # If how is string, fetch function from dictionary:
    if isinstance(how, str):
        how = get_how(how)
    
    if lat_key is None:
        lat_key = get_dim_key(dataarray, 'y')
    if lon_key is None:
        lon_key = get_dim_key(dataarray, 'x')

    spatial_dims = get_spatial_dims(dataarray, lat_key, lon_key)
    
    # If latitude_weighted, build array of weights based on latitude.
    if isinstance(weights, str):
        weights = WEIGHTS_DICT[weights](dataarray, spatial_dims=spatial_dims)
        kwargs.update(dict(weights=weights))
    

    reduced_list = []
    for mask in _shape_mask_iterator(geodataframe, dataarray, **kwargs):
        this = dataarray.where(mask, other=np.nan)
        reduced = this.reduce(how, dim=spatial_dims, **kwargs).compute()
        reduced_list.append(reduced)
        # context.debug(f"Shapes.average reduced ({i}): {reduced} \n{i}")

    if isinstance(mask_dim, str):
        mask_dim_values = geodataframe.get(mask_dim, np.arange(len(reduced_list))).to_numpy()
    elif isinstance(mask_dim, dict):
        assert len(mask_dim)==1, 'If provided as a dictionary, mask_dim should have onlly one key value pair'
        mask_dim, mask_dim_values = mask_dim.items()
    else:
        raise ValueError('Unrecognised format for mask_dim, should be a string or length one dictionary')
    
    out = xr.concat(reduced_list, dim=mask_dim)
    out = out.assign_coords(coords={mask_dim: mask_dim_values})

    out.attrs.update(geodataframe.attrs)

    return out