import json
import subprocess
import sys

def load_composite_proof(paths):

    size = len(paths)
    input_lengths = []

    data = []

    for path in paths:
        proof_path = path + '/proof.json'

        with open(proof_path, 'r') as file:
            proof_data = json.load(file)

        proof_keys = {key: proof_data[key] for key in ('proof', 'inputs')}
        input_lengths.append(len(proof_keys['inputs'])) 
        data.append(proof_keys)

    with open('size.zok', 'w') as f:
        for i in range(0, len(input_lengths)):
            f.write(f'const u32 IN_{i+1} = {input_lengths[i]};\n')
    
    for path in paths:
        verification = path + '/verification.key'
        with open(verification, 'r') as file:
            verification_data = json.load(file)
        
        verification_keys = {key: verification_data[key] for key in ('h', 'g_alpha', 'h_beta', 'g_gamma', 'h_gamma', 'query')}
        data.append(verification_keys)

    with open('gm17.json', 'w') as file:
        json.dump(data, file)

    with open('nested_proof.zok', 'w') as file:
        file.write('from "snark/gm17" import main as verify, Proof, VerificationKey;\n')
        file.write('from "./size.zok" import ')
        for i in range(0, len(paths)):
            if i != len(paths) - 1:
                file.write(f'IN_{i+1},')
            else:
                file.write(f'IN_{i+1};\n')
            
        for i in range(0, len(paths)):
            file.write(f'const u32 IV_{i+1} = IN_{i+1} + 1;\n')
        
        file.write('\n')
        file.write(f'def main(')
        for i in range(0, len(paths)):
            file.write(f'Proof<IN_{i+1}> sp{i+1}, ')

        for i in range(0, len(paths)):
            if i != 0:
                file.write(f', VerificationKey<IV_{i+1}> vk{i+1}')
            else:
                file.write(f'VerificationKey<IV_{i+1}> vk{i+1}')

        file.write('){\n')
        for i in range(0, len(paths)):
            file.write(f'   assert(verify(sp{i+1}, vk{i+1}));\n')

        file.write('}\n')

def runZKP():
    subprocess.run(["zokrates", "compile", "-i", "nested_proof.zok", "--curve", "bw6_761"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content gm17.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])

def aggregate_proofs(paths):

    for path in paths:
        load_composite_proof([path])
        runZKP()
 
    with open('proof.json', 'r') as file:
        proof_data = json.load(file)
    
    
    return proof_data
          
# aggregate_proofs(['../zkDist'])
