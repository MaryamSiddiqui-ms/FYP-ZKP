import subprocess 
import json
import os

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



def zkSort(arguments, dir_path):

    curr_path = dir_path + '/zkSort'
    os.chdir(curr_path)
    
    with open('size.zok', 'w') as f:
        f.write('const u32 size = {};\n'.format(int(len(arguments)/2)))

    subprocess.run(["zokrates", "compile", "-i", "sortver.zok"])
    subprocess.run(["zokrates", "setup"])
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
        output_file.write(witness_array_line)
        
    subprocess.run(["zokrates", "generate-proof"])
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)

    witness = getWitness()

    os.chdir(curr_path)

    return proof, witness

