import subprocess 
import json
import os


def zkmaxLabel(knn_output, K, dir_path):
    # with open('maxLabel.json', 'r') as f:
    #     knn_output = json.load(f)
    curr_path = dir_path + '/zkMaxLabel'
    os.chdir(curr_path)

    label = knn_output[1::2]
    labels = list(map(str, label))
    labels = labels[0:K]

    with open('size.zok', 'w') as f:
        f.write('const u32 size = {};\n'.format(int(len(labels))))
    
    

    subprocess.run(["zokrates", "compile", "-i", "maxLabel.zok"])
    subprocess.run(["zokrates", "setup"])
    result = subprocess.run(["zokrates", "compute-witness", "--verbose", "-a"] + labels, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
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
        
    subprocess.run(["zokrates", "generate-proof"])
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)
        
    with open('witness_output.txt', 'r') as file:
        content = json.load(file)
        print("Prediction: ", content[0])

    os.chdir(curr_path)

    return proof, content[0]

