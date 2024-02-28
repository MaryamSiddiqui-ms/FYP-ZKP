def removeNegatives(arguments):
    if isinstance(arguments[0], list):
        modified_arr =  [item for sublist in arguments for item in sublist]
    else:
        modified_arr = arguments
    positive_min = abs(min(modified_arr))
    mod_arr = [(item + positive_min) for item in modified_arr]

    return mod_arr, positive_min