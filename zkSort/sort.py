import subprocess 
import json
import os
import numpy as np
import sys

def getWitness():
    with open('witness_output.txt', 'r') as file:
        content = file.read()

    try:
        python_array = json.loads(content)
        if isinstance(python_array, list):
            return python_array
        else:
            print("The content is not in array format.")
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)



def zkSort(arguments, dir_path=''):

    witness = []
    labels = []
    data = []

    print(arguments)

    list_of_integers = [[int(i) for i in sublist] for sublist in arguments]
    list_of_integers.sort(key=lambda x: x[0])
    sorted_arr = [[str(i) for i in sublist] for sublist in list_of_integers]

    print(sorted_arr)

    # for i in range(0, len(arguments)):
    #     if i % 2 == 0:
    #         witness.append(int(arguments[i]))
    #     else:
    #         labels.append(int(arguments[i]))

    # structured_arr = np.zeros(len(witness), dtype=[('witness', np.int64), ('label', int)])

    # structured_arr['witness'] = witness
    # structured_arr['label'] = labels

    # sorted_arr = np.sort(structured_arr, order='witness')
    # output = np.array([str(val) for pair in sorted_arr for val in pair])

    # output = output.tolist()

    curr_path = dir_path + '/zkSort'
    os.chdir(curr_path)
    # print("This are the arguments: ",arguments)

    with open('size.zok', 'w') as f:
        f.write('const u32 size = {};\n'.format(int(len(arguments))))

    with open('input.json', 'w') as f:
        json.dump([sorted_arr], f)

    subprocess.run(["zokrates", "compile", "-i", "sortver.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
        
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)

    # witness = getWitness()


    os.chdir(curr_path)

    return proof, sorted_arr