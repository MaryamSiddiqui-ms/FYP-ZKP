import subprocess 
import json
import os
import numpy as np
import math
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.removeNegatives import removeNegatives

def zkRelu(arguments = [[[1, 0.2, 0.03], [4, 0.5, 0.006]], [[7, 8, 9], [10, 11, 12]]] , dir_path=''):

    witness = []
    labels = []
    data = []

    print(arguments)



    modified_arr, positive_min = removeNegatives(arguments)
    mod_arr = [int(item*math.pow(10,8)) for item in modified_arr]
    str_mod_arr = [str(item) for item in mod_arr]
    sys.path.pop()

    curr_path = dir_path + '/zkRelu'
    os.chdir(curr_path)


    with open('size.zok', 'w') as f:
        f.write('const u32 size = {};\n'.format(int(len(modified_arr))))

    with open('input.json', 'w') as f:
        json.dump([str_mod_arr,str(int(positive_min))], f)

    subprocess.run(["zokrates", "compile", "-i", "relu.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
        
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)


    os.chdir(curr_path)

    return proof, modified_arr

