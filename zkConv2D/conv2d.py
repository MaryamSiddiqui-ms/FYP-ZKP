import numpy as np
import tensorflow as tf
import json
import subprocess
import sys



def summation(arr):
    tmp = arr.reshape(-1)
    sum = 0
    for i in tmp:
        sum += i
        
    return sum

def extract_filter_and_bias(weights_dict, key):
    filters = weights_dict[key][0]
    bias = weights_dict[key][1]

    if isinstance(filters, list):
        filters = np.array(filters)

    if isinstance(bias, list):
        bias = np.array(bias)

    size = len(filters[0,0,0])
    filters = np.array([filters[:, :, :, curr] for curr in range(size)])

    return (filters, bias)

def conv2d(input, filters, bias, num_filters):
    input_height, input_width, _ = input.shape
    filter_height, filter_width, _ = filters[0].shape

    output_height = input_height - filter_height + 1
    output_width = input_width - filter_width + 1

    output = np.zeros((output_height, output_width, num_filters))

    for k in range(num_filters):
        for i in range(output_height):
            for j in range(output_width):
                output[i, j, k] = summation(input[i:i+filter_height, j:j+filter_width] * filters[k]) + bias[k]

    return output



def main():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    
    with open('weights_4.json', 'r') as json_file:
        weights_dict = json.load(json_file)

    (filters_1, bias_1) = extract_filter_and_bias(weights_dict, "conv2d_19")

    inputs = x_test[20]
    inputs = np.array(inputs)
    inputs = inputs.reshape(28,28,1)
    
    out = conv2d(inputs, filters_1, bias_1, filters_1.shape[0])
    
    data = [filters_1.tolist(), bias_1.tolist(), inputs.tolist(), out.tolist()]
    
    with open('input.json', 'w') as f:
        json.dump(data, f)

    with open('size.zok', 'w') as f:
        f.write('const u32 input_size = {};\n'.format(inputs.shape[0]))
        f.write('const u32 filter_size = {};\n'.format(filters_1[0].shape[0]))
        f.write('const u32 num_filters = {};\n'.format(filters_1.shape[0]))
        f.write('const u32 channels = {};\n'.format(inputs.shape[2]))
                
    subprocess.run(["zokrates", "compile", "-i", "conv2d.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    
if __name__ == "__main__":
    main()
    