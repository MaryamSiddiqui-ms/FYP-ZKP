import subprocess 
import json
import os
import numpy as np
import sys

def zkSort(arguments, dir_path=''):

    witness = []
    labels = []
    data = []

    print(arguments)

    list_of_integers = [[int(i) for i in sublist] for sublist in arguments]
    list_of_integers.sort(key=lambda x: x[0])
    sorted_arr = [[str(i) for i in sublist] for sublist in list_of_integers]

    print(sorted_arr)


    curr_path = dir_path + '/zkSort'
    os.chdir(curr_path)


    with open('size.zok', 'w') as f:
        f.write('const u32 size = {};\n'.format(int(len(arguments))))

    with open('input.json', 'w') as f:
        json.dump([sorted_arr], f)

    subprocess.run(["zokrates", "compile", "-i", "sortver.zok"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
        
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)


    os.chdir(curr_path)

    return proof, sorted_arr