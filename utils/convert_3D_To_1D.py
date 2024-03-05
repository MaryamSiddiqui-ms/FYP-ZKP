import numpy as np

def convert_3d_to_1d(array_3d):
    if not isinstance(array_3d, np.ndarray):
        array_3d = np.array(array_3d)
    return array_3d.ravel()

