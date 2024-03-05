import subprocess
import json
import sys
import numpy as np
import math

# dot_product = np.dot(matrix1, matrix2)
# result = dot_product + bias_b
# print(result)

def get_matrix_dimensions(matrix):
    rows = len(matrix)
    columns = len(matrix[0]) if rows > 0 else 0
    return rows, columns
def zkApplyWeights(matrix1,matrix2,bias_b):

    rows1, columns1 = get_matrix_dimensions(matrix1)
    rows2, columns2 = get_matrix_dimensions(matrix2)
    rowsb,columnsb = get_matrix_dimensions(bias_b)
        
    with open('size.zok', 'w') as f:
        f.write('const u32 M1 = {};\n'.format(int(rows1)))
        f.write('const u32 N1 = {};\n'.format(int(columns1)))
        f.write('const u32 M2 = {};\n'.format(int(rows2)))
        f.write('const u32 N2 = {};\n'.format(int(columns2)))
        f.write('const u32 br = {};\n'.format(int(rowsb)))
        f.write('const u32 bc = {};\n'.format(int(columnsb)))
        
    dot_product = np.dot(matrix1, matrix2)
    result = dot_product + bias_b
    print(result)
    
    matrix_1 = list(map(lambda row: [str(int(element*math.pow(10,8))) for element in row], matrix1))
    matrix_2 = list(map(lambda row: [str(int(element*math.pow(10,8))) for element in row], matrix2))

    # bias = bias_b[0].astype(str).tolist()

    bias = [str(int(item * math.pow(10,8))) for item in bias_b[0]]  # Convert the first element of bias_b to string and store in a list


    # result = list(map(lambda row: [str(element*math.pow(10,8)) for element in row], result))
    
    with open('input.json', 'w') as f:
        json.dump([matrix_1,matrix_2,bias], f)

    print("Result of dot product of matrices with bias:")

    subprocess.run(["zokrates", "compile", "-i", "applyWeights.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin","--verbose"], stdout=sys.stdout)
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])

    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)
        
    return proof,result
    

# subprocess.run(["zokrates", "verify"])
matrix1 = np.array([["1",  "2",  "3"], ["4",  "5",  "6"]], dtype=int)
matrix2 = np.array([["7",  "8"], ["9",  "10"], ["11",  "12"]], dtype=int)
bias_b = np.array([["1", "3"]], dtype=int)

zkApplyWeights(matrix1,matrix2,bias_b)