import subprocess 
import json
import pandas as pd


df = pd.read_csv('train.csv', header=None)

flattened_data = list(map(str, df.values.ravel()))

with open('input.json', 'w') as f:
    json.dump(flattened_data, f)

def getArgsFromJson(datapoint):
    with open('input.json', 'r') as f:
        data = json.load(f)

    data.extend(map(str, datapoint))

    data = [int(x) for x in data]
    arguments = list(map(str, data))
    return arguments


def zkDistance(datapoint):
    arguments = getArgsFromJson(datapoint)
    rows = df.shape[0]
    cols = df.shape[1]

    print(rows)
    print(cols)

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




zkDistance([6, 3])