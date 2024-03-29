import sys
import json
import numpy as np
import math
import os


current_file_path = os.path.abspath(__file__)
project_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
current_pythonpath = os.environ.get('PYTHONPATH', '')
os.environ['PYTHONPATH'] = f"{project_path};{current_pythonpath}"

try: 
    sys.path.append('./zkConv2D')
    sys.path.append('./zkRelu')
    sys.path.append('./zkMaxPooling')
    sys.path.append('./zkSoftmax')
    sys.path.append('./zkArgmax')
    sys.path.append('./zkFlatten')
    sys.path.append('./zkApplyWeights')
    sys.path.append('./ProofComposition')
    sys.path.append('./utils')

    # from clean import clean_dirs
    # from extractor import extract_filter_and_bias

    # from utils.clean import clean_dirs
    from extractor import extract_filter_and_bias

    from conv2d import zkConv2D
    from relu import zkRelu
    from maxpooling import zkMaxPooling
    from softmax import zkSoftmax
    # from flatten import zkFlatten
    from applyWeights import zkApplyWeights
    from argmax import zkArgmax

    # from relu import zkRelu
    # from softmax import zkSoftmax
    # from maxpooling import zkMaxPooling
    # from argmax import zkArgmax
    # from conv2d import zkConv2D
    # from applyWeights import zkApplyWeights

except Exception as e:
    print(e)
    

def convert_to_str(arr):
    str_arr = np.vectorize(lambda x: str(int(x * math.pow(10, 4))))(arr)
    return str_arr

class CNN:
    def __init__(self, weights, inputs):
        self.weights = weights
        self.inputs = inputs
        self.execution_time = 0
        self.predicted = -1
        self.proof = {}
        
    def _setExecutionTime(self, ts):
        self.execution_time = ts
        
    def getExecutionTime(self, ts):
        return self.execution_time
    
    
    def build(self):
        self.inputs = self.inputs.reshape(28,28,1)
        
        (filters_1, bias_1) = extract_filter_and_bias(self.weights, "conv2d_19")
        (filters_2, bias_2) = extract_filter_and_bias(self.weights, "conv2d_20")
        (filters_3, bias_3) = extract_filter_and_bias(self.weights, "conv2d_21")
        dense_1 = np.array(self.weights["dense_14"][0]).transpose()
        bias_d1 = np.array(self.weights["dense_14"][1])
        dense_2 = np.array(self.weights["dense_15"][0]).transpose()
        bias_d2 = np.array(self.weights["dense_15"][1])
        
        proofs = []
        
        dir_path = os.getcwd()
        
        
        self.inputs = (self.inputs / 255.0) * (10**4)
        self.inputs = self.inputs.astype(int)


        output_1, proof1 = zkConv2D(filters_1, bias_1, self.inputs, dir_path)
        activated_1, proof2 = zkRelu(output_1, dir_path)
        pooled_1, proof3 = zkMaxPooling(activated_1, dir_path)

        output_2, proof4 = zkConv2D(filters_2, bias_2, pooled_1, dir_path)
        activated_2, proof5 = zkRelu(output_2, dir_path)
        pooled_2, proof6 = zkMaxPooling(activated_2, dir_path)

        output_3, proof7 = zkConv2D(filters_3, bias_3, pooled_2, dir_path)
        activated_3, proof8 = zkRelu(output_3, dir_path)

        flattened_layer = activated_3.flatten().reshape(-1, 1)
        output_d1, proof9 = zkApplyWeights(dense_1, flattened_layer, bias_d1, dir_path)
        output_d1.reshape(1,-1)
        activated_d1, proof10 = zkRelu(output_d1, dir_path)

        output_d2, proof11 = zkApplyWeights(dense_2, activated_d1, bias_d2, dir_path)
        activated_d2, proof12 = zkRelu(output_d2, dir_path)
        activated_d2, proof13= activated_d2.reshape(-1)
        final, proof14 = zkSoftmax(activated_d2, dir_path)
        prediction, proof15 = zkArgmax(final)

        # Aggregate proofs

        self.predicted = prediction
        self.proof = proof15
        