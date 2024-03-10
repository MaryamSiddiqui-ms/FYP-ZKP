import numpy as np
import tensorflow as tf
import json
import subprocess
import sys
import os
import math

sys.path.append('../utils')

from clean import clean_dirs
from extractor import extract_filter_and_bias

def summation(arr):
    tmp = arr.reshape(-1)
    sum = 0
    for i in tmp:
        sum += i
        
    return sum



def conv2d(input, filters, bias, num_filters):
    input_height, input_width, _ = input.shape
    filter_height, filter_width, _ = filters[0].shape

    output_height = input_height - filter_height + 1
    output_width = input_width - filter_width + 1

    output = np.zeros((output_height, output_width, num_filters), dtype='int')

    for k in range(num_filters):
        for i in range(output_height):
            for j in range(output_width):
                output[i, j, k] = summation(input[i:i+filter_height, j:j+filter_width] * filters[k]) + bias[k]

    return output



def zkConv2D(filter, bias, input, dir_path=''):
    curr_path = dir_path + '/zkConv2D'
    os.chdir(curr_path)
    
    min_val = filter.min()
    if min_val < 0:
        filter += abs(min_val)
    filter_nor = filter * math.pow(10,4)
    

    filter_int = filter_nor.astype(int)    
    filter_str = filter_int.astype(str)

    if bias.min() < 0:
        bias += abs(bias.min())
    bias_nor = bias * math.pow(10,4)
    bias_int = bias.astype(int)
    bias_str = bias_int.astype(str)

    if input.min() < 0:
        input += abs(input.min())
    input_nor = input * math.pow(10,4)
    input_int = input_nor.astype(int)
    input_str = input_int.astype(str)

    out = conv2d(input_int, filter_int, bias_int, filter_int.shape[0])
    
    out_int = out.astype(int)
    out_str = out.astype(str)
    data = [filter_str.tolist(), bias_str.tolist(), input_str.tolist(), out_str.tolist()]
    
    with open('input.json', 'w') as f:
        json.dump(data, f)

    with open('size.zok', 'w') as f:
        f.write('const u32 input_size = {};\n'.format(input.shape[0]))
        f.write('const u32 filter_size = {};\n'.format(filter[0].shape[0]))
        f.write('const u32 num_filters = {};\n'.format(filter.shape[0]))
        f.write('const u32 channels = {};\n'.format(input.shape[2]))
                
    subprocess.run(["zokrates", "compile", "-i", "conv2d.zok"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)
    
    os.chdir(dir_path)
    
    return out_int, proof
    

    