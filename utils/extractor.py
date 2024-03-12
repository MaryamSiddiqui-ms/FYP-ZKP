import numpy as np

def extract_filter_and_bias(weights_dict, key):
    filters = weights_dict[key][0]
    bias = weights_dict[key][1]

    if isinstance(filters, list):
        filters = np.array(filters)

    if isinstance(bias, list):
        bias = np.array(bias)

    size = len(filters[0,0,0])
    filters = np.array([filters[:, :, :, curr] for curr in range(size)])

    return (filters, bias)