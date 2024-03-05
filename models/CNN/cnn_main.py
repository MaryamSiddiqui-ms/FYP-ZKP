from CNN import CNN

def getModelParams(file_path):
    with open(file_path, 'r') as json_file:
        weights_dict = json.load(json_file)
        
    return weights_dict

def convert_to_str(arr):
    str_arr = np.vectorize(lambda x: str(int(x * math.pow(10, 8))))(arr)
    return str_arr

def generateProofCnn(input_image):
    params_file = 'weights_4.json'
    weights_dict = getModelParams(params_file)
    
    weights_dict = convert_to_str(weights_dict)
    input_image = convert_to_str(input_image)
    
    model = CNN(weights_dict, input_image)
    
    model.build()
    return model.predicted, model.proof
    
    
    
    
    
    
