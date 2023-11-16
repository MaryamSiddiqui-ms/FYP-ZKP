import subprocess 
import json

"""
    Takes 6 integers [ 5 for the private array, and 1 for the public index ]
    Outputs: Proof.
"""

with open('distance.json', 'r') as f:
    data = json.load(f)

data = [int(x) for x in data]
arguments = list(map(str, data))

def zkArgmax():
    subprocess.run(["zokrates", "compile", "-i", "argmax.zok"])
    subprocess.run(["zokrates", "setup"])
    subprocess.run(["zokrates", "compute-witness", "--verbose", "-a"] + arguments)
    subprocess.run(["zokrates", "generate-proof"])

    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)
    
    print(proof)


size = 3

with open('size.zok', 'w') as f:
    f.write('const u32 size = {};\n'.format(size))

zkArgmax()