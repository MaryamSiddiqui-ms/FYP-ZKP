from convert_3D_To_1D import convert_3d_to_1d

def removeNegatives(arguments):
    if isinstance(arguments, list):
        modified_arr = convert_3d_to_1d(arguments)
    else:
        modified_arr = arguments
        
    if modified_arr.min() < 0:
        positive_min = abs(modified_arr.min())
        mod_arr = [(item + positive_min) for item in modified_arr]
    else:
        mod_arr = modified_arr
        positive_min = 0
        
    return mod_arr, positive_min