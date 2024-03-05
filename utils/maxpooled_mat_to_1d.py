
def convert_pooled_mat_to_1d(pooled_mat):
    shape = pooled_mat.shape
    pooled_mat_reshaped = pooled_mat.reshape((shape[0] * shape[1], shape[2]))
    pooled_mat_1d = pooled_mat_reshaped.flatten()
    return pooled_mat_1d
