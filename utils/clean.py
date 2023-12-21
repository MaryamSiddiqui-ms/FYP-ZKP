import os
import glob

def clean_dirs(directories):
    filenames = ['abi.json', 'out', 'out.r1cs', 'out.wtns', 'proof.json', 'proving.key', 'verification.key', 'witness', 'witness_output.txt', 'size.zok', 'input.json', 'gm17.json', 'nested_proof.zok']

    for directory in directories:
        for filename in filenames:
            for file_path in glob.glob(os.path.join(directory, filename)):
                os.remove(file_path)



dir_paths = ['./','../zkDist', '../zkSort', '../zkMaxLabel', '../', '../ProofComposition']
clean_dirs(dir_paths)