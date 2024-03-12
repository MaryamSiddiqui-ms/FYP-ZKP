import subprocess 
import json
import pandas as pd
import os
import numpy as np
import sys
# from minMaxNormalizationAndInteger import minMaxNormalizationAndInteger

def getArgsFromJson():
    with open('input.json', 'r') as f:
        data = json.load(f)

    data = [int(x) for x in data]
    arguments = list(map(str, data))
    arguments.pop()
    return arguments

def getDistance(row1, row2):
    distance = np.int64(0)

    distance = (row1[0] - row2[0])**2 + (row1[1] - row2[1])**2

    return [distance, row2[2]]



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



def zkDistance(normd_df, dir_path=''):
    
    curr_path = dir_path + '/zkDist'
    os.chdir(curr_path)

    data = []
    distances=[]

    flattened_data = list(map(str, normd_df.values.ravel()))

    dp0 = normd_df.values[-1][0]
    dp1 = normd_df.values[-1][1]

    dp = [dp0, dp1]

    for value in normd_df.values[:-1]:
        distances.append(getDistance(dp, value))


    output = np.array([[str(pair[0]), str(pair[1])] for pair in distances])
    output = output.tolist()

    dp = [str(dp0), str(dp1)]

    df_list = normd_df[:-1].values.tolist()
    df_list = [list(map(str, sublist)) for sublist in df_list]

    data.append(df_list)
    data.append(dp)
    data.append(output)


    rows = normd_df.shape[0] - 1
    cols = normd_df.shape[1]

    with open('input.json', 'w') as f:
        json.dump(data, f)

    with open('size.zok', 'w') as f:
        f.write('const u32 rows = {};\n'.format(rows))
        f.write('const u32 cols = {};\n'.format(cols))
        f.write('const u32 test = {};\n'.format(cols-1))

    subprocess.run(["zokrates", "compile", "-i", "distance.zok"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)

    os.chdir(dir_path)
    
    return proof, output    

def testFun():
    subprocess.run(["zokrates", "compile", "-i", "test.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)

