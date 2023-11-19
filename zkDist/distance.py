import subprocess 
import json
import pandas as pd

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

def zkDistance(datapoint, df):
    
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

    subprocess.run(["zokrates", "compile", "-i", "distance.zok"])
    subprocess.run(["zokrates", "setup"])
    subprocess.run(["zokrates", "compute-witness", "--verbose", "-a"] + arguments)
    subprocess.run(["zokrates", "generate-proof"])

    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)
    
    print(proof)

df = pd.read_csv('train.csv', header=None)


zkDistance([6, 3], df)