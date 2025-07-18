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
    """

    items_count = df.shape[1]
    data = df.dropna()
    variance_sum = float(data.var(axis=0, ddof=1).sum())
    total_var = float(data.sum(axis=1).var(ddof=1))

    return np.round(items_count / float(items_count - 1) * (1 - variance_sum / total_var), 3)

