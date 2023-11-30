import subprocess 
import json
import pandas as pd
import os
import numpy as np

def getArgsFromJson():
    with open('input.json', 'r') as f:
        data = json.load(f)

    data = [int(x) for x in data]
    arguments = list(map(str, data))
    arguments.pop()
    return arguments

def minMaxNormalizationAndInteger(df):
    for column in df.columns:
        if df[column].dtype == 'float64':

            min_val = df[column].min()
            max_val = df[column].max()
            df[column] = (df[column] - min_val) / (max_val - min_val)
            df[column] = df[column].round(8)
            df[column] = (df[column] * 10**8).astype(int)

    return df


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



def zkDistance(df, datapoint, dir_path=''):
    
    curr_path = dir_path + '/zkDist'
    os.chdir(curr_path)

    datapoint.append(-1)
    df.loc[len(df)] = datapoint   
 
    distances = []
    normd_df = minMaxNormalizationAndInteger(df)
    dp0 = normd_df.values[-1][0]
    dp1 = normd_df.values[-1][1]
    dp = [dp0, dp1]
    for value in normd_df.values[:-1]:
        distances.append(getDistance(dp, value))


    output = np.array([str(val) for pair in distances for val in pair])
    output = output.tolist()


    flattened_data = list(map(str, normd_df.values.ravel()))
    with open('input.json', 'w') as f:
        json.dump(flattened_data, f)

    arguments = getArgsFromJson()

    arguments += output

    rows = normd_df.shape[0] - 1
    cols = normd_df.shape[1]


    with open('size.zok', 'w') as f:
        f.write('const u32 rows = {};\n'.format(rows))
        f.write('const u32 cols = {};\n'.format(cols))
        f.write('const u32 test = {};\n'.format(cols-1))

    subprocess.run(["zokrates", "compile", "-i", "distance.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["zokrates", "compute-witness", "--verbose", "-a"] + arguments)
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)

    os.chdir(curr_path)
    
    return proof, output    
