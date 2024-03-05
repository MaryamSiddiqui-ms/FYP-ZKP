from CNN import CNN
import json
import numpy as np
import math

def getModelParams(file_path):
    with open(file_path, 'r') as json_file:
        weights_dict = json.load(json_file)
        
    return weights_dict


def generateProofCnn(input_image):
    params_file = 'weights_4.json'
    weights_dict = getModelParams(params_file)
    
    weights_dict = convert_to_str(weights_dict)
    input_image = convert_to_str(input_image)
    
    # model = CNN(weights_dict, input_image)
    
    # model.build()
    # return model.predicted, model.proof


generateProofCnn([[0.1,0.03],[0.001,0.009]])
    
    
    
    
    
    
