# Example additional functions for statistical calculations
import numpy as np
import pandas as pd
from typing import List, Dict, Any

def descriptive_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate descriptive statistics for the passed dataframe.

    Args:
        df (pd.DataFrame): Items with each column as a variable and each row as an observation.

    Returns:
        Dict[str, Any]: Dictionary containing descriptive statistics.
    """
    
    data = df.dropna()
    
    return {
        "mean": data.mean().to_dict(),
        "median": data.median().to_dict(),
        "std": data.std().to_dict(),
        "variance": data.var().to_dict(),
        "min": data.min().to_dict(),
        "max": data.max().to_dict(),
        "count": data.count().to_dict(),
        "skewness": data.skew().to_dict(),
        "kurtosis": data.kurtosis().to_dict()
    }

def correlation_matrix(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate correlation matrix for the passed dataframe.

    Args:
        df (pd.DataFrame): Items with each column as a variable and each row as an observation.

    Returns:
        Dict[str, Any]: Dictionary containing correlation matrix and related statistics.
    """
    
    data = df.dropna()
    corr_matrix = data.corr()
    
    return {
        "correlation_matrix": corr_matrix.to_dict(),
        "mean_correlation": float(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean()),
        "max_correlation": float(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].max()),
        "min_correlation": float(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].min())
    }

def item_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """Perform item analysis including item-total correlations.

    Args:
        df (pd.DataFrame): Items with each column as a variable and each row as an observation.

    Returns:
        Dict[str, Any]: Dictionary containing item analysis results.
    """
    
    data = df.dropna()
    total_score = data.sum(axis=1)
    
    item_total_correlations = {}
    item_rest_correlations = {}
    
    for column in data.columns:
        # Item-total correlation
        item_total_correlations[column] = float(data[column].corr(total_score))
        
        # Item-rest correlation (correlation with total minus the item itself)
        rest_score = total_score - data[column]
        item_rest_correlations[column] = float(data[column].corr(rest_score))
    
    return {
        "item_total_correlations": item_total_correlations,
        "item_rest_correlations": item_rest_correlations,
        "item_means": data.mean().to_dict(),
        "item_std": data.std().to_dict()
    }
