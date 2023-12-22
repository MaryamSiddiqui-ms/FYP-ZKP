import pandas as pd
import numpy as np


def minMaxNormalizationAndInteger(df):
    for column in df.columns:
        if df[column].dtype == 'float64':

            min_val = df[column].min()
            max_val = df[column].max()
            df[column] = (df[column] - min_val) / (max_val - min_val)
            df[column] = df[column].round(8)
            df[column] = (df[column] * 10**8).astype(int)

    return df