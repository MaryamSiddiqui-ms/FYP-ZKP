from CNN import CNN
import json
import numpy as np
import math
import sys
import time


def getModelParams(file_path):
    with open(file_path, 'r') as json_file:
        weights_dict = json.load(json_file)
        
    return weights_dict


def generateProofCnn(input_image):
    params_file = 'weights_5.json'
    weights_dict = getModelParams(params_file)
    
    start = time.time()
    model = CNN(weights_dict, input_image)
    model.buildWithoutZok()
    end = time.time()
    
    execution_time = (end - start)
    print("EXECUTION TIME: ", execution_time)
    
    return model.predicted, model.proof


# generateProofCnn(np.random.randint(0, 256, size=(28, 28)))
    
    
    
    
    
    
