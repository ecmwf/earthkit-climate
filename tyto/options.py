import numpy as np

def nanaverage(
    data,
    weights=None,
    axis=None,
    **kwargs
):
    '''
    A merge of the functionality of np.nanmean and np.average. 
    It returns the mean of the data with correct handling of nan
    values (nanmean), and it accepts a weights argument (average)

    Args:
        data : numpy array
        weights: Weights to apply to the data for averaging. 
            Weights will be normalised and must correspond to the
            shape of the numpy data array and axis/axes that is/are
            averaged over.
        axis: axis/axes to compute the nanaverage over.
        kwargs: any other np.nansum kwargs
    Returns:
        weights equal to cosine of latitude coordinate
    '''
    if weights is not None:
        # set weights to nan where data is nan:
        this_weights = np.ones(data.shape)*weights
        this_weights[np.isnan(data)] = np.nan

        # Weights must be scaled to the mean of valid
        #  weights for each relevant axis:
        this_denom = np.nansum(
            this_weights, **kwargs
        )
        # If averaging over axis/axes then we must add dummy
        # dimension[s] to the denominator to make compatible
        # with the weights.
        if axis is not None:
            reshape = list(this_weights.shape)
            for a in axis:
                reshape[a] = 1
            this_denom = this_denom.reshape(reshape)
        
        # Scale weights to mean of valid weights:
        this_weights = (
            this_weights/this_denom
        )
        # Apply weights to data:
        nanaverage = np.nansum(
            data * this_weights, **kwargs
        )
    else:
        nanaverage = np.nanmean(data, **kwargs)

    return nanaverage


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