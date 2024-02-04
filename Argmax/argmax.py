import subprocess 
import json

"""
    Takes 6 integers [ 5 for the private array, and 1 for the public index ]
    Outputs: Proof.
"""

with open('argmax.json', 'r') as f:
    data = json.load(f)

data = [int(x) for x in data]
arguments = list(map(str, data))

max_index = data.index(max(data))
print("MAX", max_index)

arguments.append(str(max_index))
print(arguments)

# with open('size.zok', 'w') as f:
#         f.write('const u32 size = {};\n'.format(int(len(arguments))))

def zkArgmax():
    subprocess.run(["zokrates", "compile", "-i", "argmax.zok","--curve", "bls12_377"])
    # subprocess.run(["zokrates", "setup"])
    # subprocess.run(["zokrates", "compute-witness", "-a"] + arguments)
    # subprocess.run(["zokrates", "generate-proof"])
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
        output_file.write( witness_array_line )
        
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)
    
    # print(proof)
    
    with open('witness_output.txt', 'r') as file:
        content = json.load(file)
        print("Prediction: ", content[0])


size = 5

with open('size.zok', 'w') as f:
    f.write('const u32 size = {};\n'.format(size))

zkArgmax()