import numpy as np
import math

def extract_filter_and_bias(weights_dict, key):
    filters = weights_dict[key][0]
    bias = weights_dict[key][1]

    if isinstance(filters, list):
        filters = np.array(filters)

    if isinstance(bias, list):
        bias = np.array(bias)

    size = len(filters[0,0,0])
    filters = np.array([filters[:, :, :, curr] for curr in range(size)])
    
    
    min_val = filters.min()
    if min_val < 0:
        filters += abs(min_val)
    filters = filters * math.pow(10,4)
    filters = filters.astype(int)
    
    if bias.min() < 0:
        bias += abs(bias.min())
    bias = bias * math.pow(10,4)
    bias = bias.astype(int)

    return (filters, bias)