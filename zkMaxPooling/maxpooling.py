import subprocess 
import json
import os
import numpy as np
import math
import sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# from utils.removeNegatives import removeNegatives
# from utils.activated_mat_to_1d import append_subarrays, convert_to_1d, sub_1d
# from utils.maxpooled_mat_to_1d import convert_pooled_mat_to_1d
# from utils.convert_3D_To_1D import convert_3d_to_1d


try:
    sys.path.append('../utils')

    from convert_3D_To_1D import convert_3d_to_1d
    from removeNegatives import removeNegatives
    from activated_mat_to_1d import append_subarrays, convert_to_1d, sub_1d
    from maxpooled_mat_to_1d import convert_pooled_mat_to_1d

except Exception as e:
    print(e)

def maxPool_2d(mat, pool_size):
    res_height = mat.shape[0] // pool_size
    res_width = mat.shape[1] // pool_size

    pooled_mat = np.zeros((res_height, res_width, mat.shape[2]), dtype=int)

    for i in range(0, mat.shape[0] - pool_size +  1, pool_size):
        for j in range(0, mat.shape[1] - pool_size +  1, pool_size):
            for k in range(0, mat.shape[2]):
                pooled_mat[i // pool_size, j // pool_size, k] = np.max(mat[i:i+pool_size, j:j+pool_size, k])

    return pooled_mat

def zkMaxPooling(arguments, dir_path=''):

    witness = []
    labels = []
    data = []

    # print(arguments)
    act_arr = convert_3d_to_1d(arguments)
    activated = np.array(act_arr)
    pool = maxPool_2d(activated,2)
    pooled = np.array(pool)

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
    mod_act_arr = [(item) for item in mod_activated]
    str_mod_act_arr = [str(item) for item in mod_act_arr]

    # modified_pool_arr, positive_min = removeNegatives(mod_pooled)
    mod_pool_arr = [(item) for item in mod_pooled]
    str_mod_pool_arr = [str(item) for item in mod_pool_arr]
    sys.path.pop()

    curr_path = dir_path + '/zkMaxPooling'
    os.chdir(curr_path)


    with open('size.zok', 'w') as f:
        f.write('const u32 size1 = {};\n'.format(int(len(mod_activated))))
        f.write('const u32 size2 = {};\n'.format(int(len(mod_pooled))))


    # with open('size2.zok', 'w') as f:
    #     f.write('const u32 size2 = {};\n'.format(int(len(mod_pooled))))

    with open('input.json', 'w') as f:
        json.dump([str_mod_act_arr,str_mod_pool_arr,str(4)], f)

    subprocess.run(["zokrates", "compile", "-i", "maxpooling.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
        
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)


    os.chdir(dir_path)

    return proof, pool


