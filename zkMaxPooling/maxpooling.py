import subprocess 
import json
import os
import numpy as np
import sys

def zkRelu(arguments , dir_path=''):

    witness = []
    labels = []
    data = []

    print(arguments)

    if isinstance(arguments[0], list):
        modified_arr =  [item for sublist in arguments for item in sublist]
    else:
        modified_arr = arguments
    positive_min = abs(min(modified_arr))
    mod_arr = [(item + positive_min) for item in modified_arr]
    str_mod_arr = [str(item) for item in mod_arr]
    print(str_mod_arr)


    curr_path = dir_path + '/zkMaxPooling'
    os.chdir(curr_path)


    with open('size.zok', 'w') as f:
        f.write('const u32 size = {};\n'.format(int(len(modified_arr))))

    with open('input.json', 'w') as f:
        json.dump([str_mod_arr,str(positive_min)], f)

    subprocess.run(["zokrates", "compile", "-i", "maxpooling.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
        
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)


    os.chdir(curr_path)

    return proof, modified_arr


