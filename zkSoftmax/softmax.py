import subprocess 
import json
import os
import numpy as np
import sys
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.removeNegatives import removeNegatives
from utils.convert_3D_To_1D import convert_3d_to_1d

def softmax(x):
  exp_x = np.exp(x - np.max(x))
  return exp_x / np.sum(exp_x)

def zkSoftmax(arguments , dir_path=''):

    witness = []
    labels = []
    data = []

    print(arguments)

    arr = zkSoftmax(arguments)

    mod_arr = convert_3d_to_1d(arr)
    # mod_arr = [item for item in arr]
    modified_arr, positive_min = removeNegatives(mod_arr)
    # mod_arr = [int(item*math.pow(10,8)) for item in modified_arr]
    str_mod_arr = [str(item) for item in modified_arr]
    sys.path.pop()

    curr_path = dir_path + '/zkSoftmax'
    os.chdir(curr_path)

    hp = ((positive_min * math.pow(10,8))/2) - positive_min

    with open('size.zok', 'w') as f:
        f.write('const u32 size = {};\n'.format(int(len(modified_arr))))

    with open('input.json', 'w') as f:
        json.dump([str_mod_arr,str(int(positive_min)),str(int(math.pow(10,8)))], f)

    subprocess.run(["zokrates", "compile", "-i", "softmax.zok"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
        
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)


    os.chdir(curr_path)

    return proof, arr


