import subprocess 
import json
import os
from collections import Counter

def zkmaxLabel(knn_output, K, dir_path):
   
    curr_path = dir_path + '/zkMaxLabel'
    os.chdir(curr_path)



    truncated = knn_output[:K]
    labels = [sublist[1] for sublist in truncated]

    
    counter = Counter(labels)
    max_label = counter.most_common(1)[0][0]
   

    labels.append(max_label)
    
    with open('size.zok', 'w') as f:
        f.write('const u32 size = {};\n'.format(int(len(labels))))
    print("Max Label: ", labels)
    subprocess.run(["zokrates", "compile", "-i", "maxLabel.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
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
        
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)
        
    with open('witness_output.txt', 'r') as file:
        content = json.load(file)
        print("Prediction: ", content[0])

    os.chdir(dir_path)

    return proof, content[0]
