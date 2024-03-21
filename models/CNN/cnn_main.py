from CNN import CNN
import json
import numpy as np
import math
import sys


def getModelParams(file_path):
    with open(file_path, 'r') as json_file:
        weights_dict = json.load(json_file)
        
    return weights_dict


def generateProofCnn(input_image):
    input_image=np.array(input_image)
    params_file = './models/cnn/weights_4.json'
    weights_dict = getModelParams(params_file)
    
    model = CNN(weights_dict, input_image)
    
    model.build()
    return model.predicted, model.proof


# generateProofCnn(np.random.randint(0, 256, size=(28, 28)))
    
    
    
    
    
    
