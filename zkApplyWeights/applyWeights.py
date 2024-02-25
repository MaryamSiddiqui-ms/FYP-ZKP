import subprocess
import json
import sys
import numpy as np

matrix1 = np.array([["1",  "2",  "3"], ["4",  "5",  "6"]], dtype=int)
matrix2 = np.array([["7",  "8"], ["9",  "10"], ["11",  "12"]], dtype=int)
bias_b = np.array([["1", "3"]], dtype=int)
dot_product = np.dot(matrix1, matrix2)
result = dot_product + bias_b
print(result)


matrix_1 = list(map(lambda row: [str(element) for element in row], matrix1))
matrix_2 = list(map(lambda row: [str(element) for element in row], matrix2))
bias = bias_b[0].astype(str).tolist()
result = list(map(lambda row: [str(element) for element in row], result))

print("Result of dot product of matrices with bias:")

subprocess.run(["zokrates", "compile", "-i", "applyWeights.zok", "--curve", "bls12_377"])
subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])


# data=[]
# data.append(matrix_1)
# data.append(matrix_2)
# data.append(bias)
# data.append(result)

# # Write data to JSON file
# with open('input.json', 'w') as f:
#     json.dump(data, f)


# Compute witness
subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin","--verbose"], stdout=sys.stdout)


subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])

with open("proof.json", 'r') as proof_file:
    proof = json.load(proof_file)
    

# subprocess.run(["zokrates", "verify"])
