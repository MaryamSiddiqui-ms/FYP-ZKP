import json
import subprocess

def load_composite_proof(paths):

    size = len(paths)
    # with open('size.zok', 'w') as f:
    #     f.write('const u32 size = {};\n'.format(size))

    combined_proofs = []
    combined_vk = []
    combined_data = []

    for path in paths:
        proof_path = path + '/proof.json'
        with open(proof_path, 'r') as file:
            proof_data = json.load(file)
        
        proof_keys = {key: proof_data[key] for key in ('proof', 'inputs')}
        input_length = len(proof_keys['inputs'])
        print(input_length)
        combined_proofs.append(proof_keys)

    
    for path in paths:
        verification = path + '/verification.key'
        with open(verification, 'r') as file:
            verification_data = json.load(file)
        
        print(verification_data)
        verification_keys = {key: verification_data[key] for key in verification_data.keys() - {'scheme', 'curve'}}
        combined_vk.append(verification_keys)

    combined_data = [combined_proofs, combined_vk]

    # # for path in paths:
    # #     proof_path = path + '/proof.json'
    # #     verification_path = path + '/verification.key'
    
    # #     with open(proof_path, 'r') as file:
    # #         proof_data = json.load(file)

    # #     with open(verification_path, 'r') as file:
    # #         verification_data = json.load(file)

    # #     proof_keys = {key: proof_data[key] for key in ('inputs', 'proof')}
    # #     verification_keys = {key: verification_data[key] for key in verification_data.keys() - {'scheme', 'curve'}}
    # #     combined_data = [proof_keys, verification_keys]

    with open('gm17.json', 'w') as file:
        json.dump(combined_data, file)

def run_proof(paths):
    # subprocess.run(["zokrates", "compile", "-i", "nested_proof.zok"])
    # subprocess.run(["zokrates", "setup"])
    load_composite_proof(paths)

if __name__ == "__main__":
    paths = ['../zkDist']
    run_proof(paths)