import sys
import json
import numpy as np

try: 
    sys.path.append('../../zkConv2D')
    sys.path.append('../../zkRelu')
    sys.path.append('../../zkSoftmax')
    sys.path.append('../../zkMaxPool2D')
    sys.path.append('../../zkArgmax')
    sys.path.append('../../zkFlatten')
    sys.path.append('../../zkApplyWeights')
    sys.path.append('../../ProofComposition')
    sys.path.append('../../utils')

    from clean import clean_dirs
    from extractor import extract_filter_and_bias
    
    from conv2d import zkConv2D
    from relu import zkRelu
    from softmax import zkSoftmax
    from flatten import zkFlatten
    from apply_weights import zkApplyWeights
    from maxpool2d import zkMaxPool2D
    from argmax import zkArgmax

except Exception as e:
    print(e)
    

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
    
    
    def build():
        self.inputs.reshape(28,28,1)
        (filters_1, bias_1) = extract_filter_and_bias(weights_dict, "conv2d_19")
        (filters_2, bias_2) = extract_filter_and_bias(weights_dict, "conv2d_20")
        (filters_3, bias_3) = extract_filter_and_bias(weights_dict, "conv2d_21")
        dense_1 = np.array(weights_dict["dense_14"][0]).transpose()
        bias_d1 = np.array(weights_dict["dense_14"][1])
        dense_2 = np.array(weights_dict["dense_15"][0]).transpose()
        bias_d2 = np.array(weights_dict["dense_15"][1])
        
        proofs = []
        
        output1, proof1 = zkConv2D(filters_1, bias_1, self.inputs)
        activated_1, proof2 = zkRelu(output_1)
        pooled_1, proof3 = zkMaxPool2D(activated_1, 2)

        output_2, proof4 = zkConv2D(filters_2, bias_2, pooled_1)
        activated_2, proof5 = zkRelu(output_2)
        pooled_2, proof6 = zkMaxPool2D(output_2, 2)

        output_3, proof7 = zkConv2D(filters_3, bias_3, pooled_2)
        activated_3, proof8 = zkRelu(output_3)

        flattened_layer = activated_3.flatten().reshape(-1, 1)
        output_d1, proof9 = zkApplyWeights(dense_1, flattened_layer, bias_d1)
        output_d1.reshape(1,-1)
        activated_d1, proof10 = zkRelu(output_d1)

        output_d2, proof11 = zkApplyWeights(dense_2, output_d1, bias_d2)
        activated_d2, proof12 = zkRelu(output_d2)
        activated_d2, proof13= activated_d2.reshape(-1)
        final, proof14 = zkSoftmax(activated_d2)
        prediction, proof15 = zkArgmax(final)

        # Aggregate proofs

        self.predicted = prediction
        self.proof = proof16
        