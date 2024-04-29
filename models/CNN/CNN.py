import sys
import json
import numpy as np
import math
import time
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
    
def conv2d(input, filters, bias, num_filters):
    input_height, input_width, _ = input.shape
    filter_height, filter_width, _ = filters[0].shape

    output_height = input_height - filter_height + 1
    output_width = input_width - filter_width + 1

    output = np.zeros((output_height, output_width, num_filters))

    for k in range(num_filters):
        for i in range(output_height):
            for j in range(output_width):
                output[i, j, k] = np.sum(input[i:i+filter_height, j:j+filter_width] * filters[k]) + bias[k]

    return output

def maxPool_2d(mat, pool_size):
    res_height = mat.shape[0] // pool_size
    res_width = mat.shape[1] // pool_size

    pooled_mat = np.zeros((res_height, res_width, mat.shape[2]), dtype=np.int64)

    for i in range(0, mat.shape[0] - pool_size +  1, pool_size):
        for j in range(0, mat.shape[1] - pool_size +  1, pool_size):
            for k in range(0, mat.shape[2]):
                pooled_mat[i // pool_size, j // pool_size, k] = np.max(mat[i:i+pool_size, j:j+pool_size, k])

    return pooled_mat

def flatten(mat):
  flattened_mat = mat.flatten()
  return flattened_mat


def apply_weights(inputs, weights, biases):
  weighted_sum = np.dot(inputs, weights)
  for i in range(weighted_sum.shape[0]):
    weighted_sum[i, 0] += biases[i]
  return weighted_sum


def relu(arr):
  return np.maximum(0, arr)

def softmax(x):
  exp_x = np.exp(x - np.max(x))
  return exp_x / np.sum(exp_x)

def argmax(x):
  return np.argmax(x)

def sum(arr):
  sum = 0
  for i in arr:
    sum += i

  return sum

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
        
        (filters_1, bias_1) = extract_filter_and_bias(self.weights, "conv2d")
        (filters_2, bias_2) = extract_filter_and_bias(self.weights, "conv2d_1")
        (filters_3, bias_3) = extract_filter_and_bias(self.weights, "conv2d_2")
        dense_1 = np.array(self.weights["dense"][0]).transpose()
        bias_d1 = np.array(self.weights["dense"][1])
        dense_2 = np.array(self.weights["dense_1"][0]).transpose()
        bias_d2 = np.array(self.weights["dense_1"][1])
        
        proofs = []
        
        dir_path = os.getcwd()
        
        
        self.inputs = (self.inputs / 255.0) * (10**4)
        self.inputs = self.inputs.astype(np.int64)


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

        output_d2, proof11 = zkApplyWeights(dense_2, activated_d1, bias_d2, project_path)
        activated_d2, proof12 = zkRelu(output_d2, project_path)
        final = activated_d2.reshape(-1)
        # final, proof13 = zkSoftmax(activated_d2, project_path)
        prediction, proof15 = zkArgmax(final, project_path)

        # Aggregate proofs

        self.predicted = prediction
        self.proof = proof15
    
    def buildWithoutZok(self):
        self.inputs = self.inputs.reshape(28,28,1)
        
        self.inputs = (self.inputs / 255.0) * (10**4)
        self.inputs = self.inputs.astype(int)
        
        (filters_1, bias_1) = extract_filter_and_bias(self.weights, "conv2d")
        (filters_2, bias_2) = extract_filter_and_bias(self.weights, "conv2d_1")
        (filters_3, bias_3) = extract_filter_and_bias(self.weights, "conv2d_2")
        dense_1 = np.array(self.weights["dense"][0]).transpose()
        bias_d1 = np.array(self.weights["dense"][1])
        dense_2 = np.array(self.weights["dense_1"][0]).transpose()
        bias_d2 = np.array(self.weights["dense_1"][1])

        output_1 = conv2d(self.inputs, filters_1, bias_1, filters_1.shape[0])
        activated_1 = relu(output_1)
        pooled_1 = maxPool_2d(activated_1, 2)

        output_2 = conv2d(pooled_1, filters_2, bias_2, filters_2.shape[0])
        activated_2 = relu(output_2)
        pooled_2 = maxPool_2d(output_2, 2)

        output_3 = conv2d(pooled_2, filters_3, bias_3, filters_3.shape[0])
        activated_3 = relu(output_3)

        flattened_layer = flatten(activated_3).reshape(-1, 1)
        output_d1 = apply_weights(dense_1, flattened_layer, bias_d1)
        output_d1.reshape(1,-1)
        activated_d1 = relu(output_d1)

        output_d2 = apply_weights(dense_2, output_d1, bias_d2)
        activated_d2 = relu(output_d2).reshape(-1)
        final = softmax(activated_d2)
        prediction = argmax(final)

        print(prediction)