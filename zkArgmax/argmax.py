import subprocess 
import json
import os

def getArguments():
    with open('input.json', 'r') as f:
        data = json.load(f)

    data = [int(x) for x in data]
    arguments = list(map(str, data))

    max_index = data.index(max(data))
    print("MAX", max_index)

    arguments.append(str(max_index))
    print(arguments)
    
    return arguments

def setSize(arguments):
    size = int(len(arguments)) -1
    with open('size.zok', 'w') as f:
            f.write('const u32 size = {};\n'.format(size))

def zkArgmax(output_probs, dir_path):

    curr_path = dir_path + '/zkArgmax'
    os.chdir(curr_path)

    with open('input.json', 'w') as f:
        json.dump(output_probs.tolist(), f)
    
    arguments = getArguments()
    setSize(arguments)

    subprocess.run(["zokrates", "compile", "-i", "argmax.zok"])
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
    
    
    with open('witness_output.txt', 'r') as file:
        content = json.load(file)
        print("Prediction: ", content[0])

    os.chdir(dir_path)

    return content[0], proof

