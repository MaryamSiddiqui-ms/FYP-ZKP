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

def minMaxNormalizationAndIntegerList(lst):
    if len(lst):
        min_val = min(lst)
        max_val = max(lst)
        normalized_list = [(x - min_val) / (max_val - min_val) for x in lst]
        
        int_list = [(round(num *  10**8)) for num in normalized_list]
        
    
    return int_list


def minMaxNorm4(arr):
    max_val = arr.max()
    normalized_arr = (arr) / (max_val)
    int_arr = np.round(normalized_arr * 10**4)
    
    return int_arr.astype(int)
