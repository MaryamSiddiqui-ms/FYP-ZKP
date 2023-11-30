import subprocess 
import json
import pandas as pd
import os

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
    distance = 0
    for i in range(len(row1)-1):
        distance += (row1[i] - row2[i])**2

    return distance*distance



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



def zkDistance(df, datapoint, dir_path):
    
    curr_path = dir_path + '/zkDist'
    os.chdir(curr_path)

    datapoint.append(-1)
    df.loc[len(df)] = datapoint   
 
    normd_df = minMaxNormalizationAndInteger(df)

    

    flattened_data = list(map(str, normd_df.values.ravel()))
    with open('input.json', 'w') as f:
        json.dump(flattened_data, f)

    arguments = getArgsFromJson()

    rows = normd_df.shape[0] - 1
    cols = normd_df.shape[1]


    with open('size.zok', 'w') as f:
        f.write('const u32 rows = {};\n'.format(rows))
        f.write('const u32 cols = {};\n'.format(cols))
        f.write('const u32 test = {};\n'.format(cols-1))

    subprocess.run(["zokrates", "compile", "-i", "distance.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    result = subprocess.run(["zokrates", "compute-witness", "--verbose", "-a"] + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    output_lines = result.stdout.split('\n')
    
    witness_line = next((line for line in output_lines if "Witness:" in line), None)
    if witness_line:
        witness_index = output_lines.index(witness_line)
        witness_array_line = output_lines[witness_index + 1]
        print( witness_array_line ) 
    else:
        print("Witness not found in the output.")


    with open('witness_output.txt', 'w') as output_file:
        output_file.write( witness_array_line)

    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])

    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)


    witness = getWitness()

    os.chdir(curr_path)
    
    return proof, witness    