import subprocess 
import json
import os
import numpy as np
import math
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.removeNegatives import removeNegatives
from utils.activated_mat_to_1d import append_subarrays, convert_to_1d, sub_1d
from utils.maxpooled_mat_to_1d import convert_pooled_mat_to_1d

def zkMaxPooling(arguments = [[[[8, 7, 7, 6],
  [0, 7, 7, 7],
  [8, 0, 6, 7],
  [7, 9, 1, 9]],

 [[6, 4, 3, 5],
  [4, 5, 2, 2],
  [6, 6, 1, 8],
  [7, 0, 3, 7]],

 [[2, 8, 6, 6],
  [0, 8, 2, 1],
  [7, 9, 6, 2],
  [8, 6, 6, 2]],

 [[8, 3, 1, 7],
  [0, 6, 4, 3],
  [3, 5, 0, 0],
  [2, 4, 4, 6]]],[[[8, 7, 7, 7],
  [8, 9, 6, 9]],

 [[8, 8, 6, 7],
  [8, 9, 6, 6]]]] , dir_path=''):

    witness = []
    labels = []
    data = []

    # print(arguments)

    activated = np.array(arguments[0])
    pooled = np.array(arguments[1])

    # print(activated.shape)
    # print(pooled.shape)

    _, subarrays = append_subarrays(activated,pooled)
    sub1d = convert_to_1d(subarrays)
    sub_activated = np.array(sub1d)
    mod_activated = sub_1d(sub_activated)
    mod_pooled = convert_pooled_mat_to_1d(pooled)

    # moda = np.array(mod_activated)

    # print(moda.shape)
    # print(mod_pooled)

    # modified_act_arr, positive_min = removeNegatives(mod_activated)
    mod_act_arr = [int(item*math.pow(10,8)) for item in mod_activated]
    str_mod_act_arr = [str(item) for item in mod_act_arr]

    # modified_pool_arr, positive_min = removeNegatives(mod_pooled)
    mod_pool_arr = [int(item*math.pow(10,8)) for item in mod_pooled]
    str_mod_pool_arr = [str(item) for item in mod_pool_arr]
    sys.path.pop()

    curr_path = dir_path + '/zkMaxPooling'
    # os.chdir(curr_path)


    with open('size1.zok', 'w') as f:
        f.write('const u32 size1 = {};\n'.format(int(len(mod_activated))))


    with open('size2.zok', 'w') as f:
        f.write('const u32 size2 = {};\n'.format(int(len(mod_pooled))))

    with open('input.json', 'w') as f:
        json.dump([str_mod_act_arr,str_mod_pool_arr,str(4)], f)

    subprocess.run(["zokrates", "compile", "-i", "maxpooling.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
        
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)


    # os.chdir(curr_path)

    return proof, str_mod_pool_arr


zkMaxPooling()