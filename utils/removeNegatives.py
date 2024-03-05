from .convert_3D_To_1D import convert_3d_to_1d

def removeNegatives(arguments):
    if isinstance(arguments[0], list):
        modified_arr = convert_3d_to_1d(arguments)
    else:
        modified_arr = arguments
    positive_min = abs(min(modified_arr))
    mod_arr = [(item + positive_min) for item in modified_arr]

    return mod_arr, positive_min