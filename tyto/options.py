import numpy as np

HOW_DICT = {
    # 'latitude_weighted_average': latitude_weighted_average,
    'average': nanaverage,
    'mean': np.nanmean,
    'stddev': np.nanstd,
    'std': np.nanstd,
    'stdev': np.nanstd,
    'sum': np.nansum,
    'max': np.nanmax,
    'min': np.nanmin,
    'median': np.nanmedian,
    'q': np.nanquantile,
    'quantile': np.nanquantile,
    'percentile': np.nanpercentile,
    'p': np.nanpercentile,
}