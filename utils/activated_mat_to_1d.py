import numpy as np

def append_subarrays(mat, pooled_mat):
    subarrays = []
    for i in range(pooled_mat.shape[0]):
        for j in range(pooled_mat.shape[1]):
            for k in range(pooled_mat.shape[2]):
                pool_i = i * mat.shape[0] // pooled_mat.shape[0]
                pool_j = j * mat.shape[1] // pooled_mat.shape[1]
                subarray = mat[pool_i:pool_i + mat.shape[0] // pooled_mat.shape[0],
                               pool_j:pool_j + mat.shape[1] // pooled_mat.shape[1],
                               k]
                subarrays.append(subarray)
    return len(subarray), subarrays

def convert_to_1d(subarrays):
    subarrays_1d = []
    for subarray in subarrays:
        subarray_1d = subarray.flatten()
        subarrays_1d.append(subarray_1d)
    return subarrays_1d

def sub_1d(arr):
    return arr.flatten()