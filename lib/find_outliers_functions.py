import numpy as np


def outliers_iqr_mod(data, feature, log_scale=False, left=1.5, right=1.5):
    """
    Tukey algorithm modified function for outlier detection.

    Parameters:
    - data (DataFrame): The DataFrame containing the dataset.
    - feature (str): The name of the column containing the feature to analyze.
    - log_scale (bool, optional): Whether to apply a logarithmic transformation to the feature. Default is False.
    - left (float, optional): The multiplier to adjust the left boundary for outlier detection. Default is 1.5.
    - right (float, optional): The multiplier to adjust the right boundary for outlier detection. Default is 1.5.

    Returns:
    - outliers (DataFrame): Subset of the original data containing outliers based on the modified Tukey algorithm.
    - cleaned (DataFrame): Subset of the original data with outliers removed based on the modified Tukey algorithm.
    """
    if log_scale:
        x = np.log(data[feature]+1)
    else:    
        x = data[feature]
    quartile_1, quartile_3 = x.quantile(0.25), x.quantile(0.75),
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * left)
    upper_bound = quartile_3 + (iqr * right)
    outliers = data[(x < lower_bound) | (x > upper_bound)]
    cleaned = data[(x >= lower_bound) & (x <= upper_bound)]
    return outliers, cleaned    


def outliers_z_score_mod(data, feature, log_scale=False, left=3,right=3):
    """
    Z-score algorithm modified function for outlier detection.

    Parameters:
    - data (DataFrame): The DataFrame containing the dataset.
    - feature (str): The name of the column containing the feature to analyze.
    - log_scale (bool, optional): Whether to apply a logarithmic transformation to the feature. Default is False.
    - left (float, optional): The number of standard deviations to the left of the mean to set the lower bound for outlier detection. Default is 3.
    - right (float, optional): The number of standard deviations to the right of the mean to set the upper bound for outlier detection. Default is 3.

    Returns:
    - outliers (DataFrame): Subset of the original data containing outliers based on the modified Z-score algorithm.
    - cleaned (DataFrame): Subset of the original data with outliers removed based on the modified Z-score algorithm.
    """
    if log_scale:
        x = np.log(data[feature]+1)
    else:
        x = data[feature]
    mu = x.mean()
    sigma = x.std()
    lower_bound = mu - left * sigma
    upper_bound = mu + right * sigma
    outliers = data[(x < lower_bound) | (x > upper_bound)]
    cleaned = data[(x >= lower_bound) & (x <= upper_bound)]
    return outliers, cleaned


def get_log_scale(data, feature, log_scale):
    """
    Apply logarithmic scaling to a feature in the dataset if specified.

    Parameters:
    - data (DataFrame): The DataFrame containing the dataset.
    - feature (str): The name of the column containing the feature to apply logarithmic scaling to.
    - log_scale (bool): Whether to apply logarithmic scaling to the feature.

    Returns:
    - x (Series): The feature data with or without logarithmic scaling applied.
    """
    if log_scale:
        if data[data[feature] == 0][feature].count():
            x = np.log(data[feature] + 1)
        else:
            x = np.log(data[feature])
    else:
        x = data[feature]
    return x


def find_z_score_parameters(data, feature, log_scale=False, left=3, right=3):
    """
    Compute Z-score parameters for outlier detection.

    Parameters:
    - data (DataFrame): The DataFrame containing the dataset.
    - feature (str): The name of the column containing the feature for which Z-score parameters are computed.
    - log_scale (bool, optional): Whether to apply logarithmic scaling to the feature. Default is False.
    - left (float, optional): The number of standard deviations to the left of the mean to set the lower bound for outlier detection. Default is 3.
    - right (float, optional): The number of standard deviations to the right of the mean to set the upper bound for outlier detection. Default is 3.

    Returns:
    - mu (float): The mean of the feature data.
    - lower_bound (float): The lower bound for outlier detection based on Z-score.
    - upper_bound (float): The upper bound for outlier detection based on Z-score.
    """
    x = get_log_scale(data, feature, log_scale)
    
    mu = x.mean()
    sigma = x.std()
    lower_bound = mu - left*sigma
    upper_bound = mu + right*sigma
    return mu, lower_bound, upper_bound
