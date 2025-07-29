# function(s) for calculating the factor's scores
import numpy as np
import pandas as pd
import polars as pl

def cronbach_alpha(df: pd.DataFrame) -> float:
    """Calculate Cronbach's alpha for the passed dataframe containing the statement scores.

    Args:
      df (pd.DataFrame): Items with each column as a variable and each row as an observation.

    Returns:
        (float): Cronbach's alpha.
        
    Raises:
        ValueError: If dataframe has less than 2 columns or insufficient data
    """
    items_count = df.shape[1]
    
    # Check if we have at least 2 items (statements)
    if items_count < 2:
        raise ValueError("Cronbach's alpha requires at least 2 items (statements)")
    
    data = df.dropna()
    
    # Check if we have sufficient data after dropping NaN values
    if data.shape[0] < 2:
        raise ValueError("Insufficient data after removing NaN values")
    
    # Check if we have any variance in the data
    variance_sum = float(data.var(axis=0, ddof=1).sum())
    total_var = float(data.sum(axis=1).var(ddof=1))
    
    # Avoid division by zero
    if total_var == 0:
        return 0.0  # No reliability if no variance
    
    return np.round(items_count / float(items_count - 1) * (1 - variance_sum / total_var), 3)

