import sys
import pandas as pd
import os
import subprocess
import time
import numpy as np

try:
    sys.path.append('./zkDist')
    sys.path.append('./zkSort')
    sys.path.append('./zkMaxLabel')
    sys.path.append('./ProofComposition')
    
    from distance import zkDistance
    from sort import zkSort
    from maxLabel import zkmaxLabel
    from proof_composition import aggregate_proofs

except Exception as e:
    print(e)


def main():
    dir_path = os.getcwd()


    df = pd.read_csv('train.csv')
    datapoint = [6,3]
    k = 3
    start_time = time.time()

    zkDistProof, distanceWitness = zkDistance(df, datapoint, dir_path)

    # result = subprocess.run(["zokrates", "verify", "-j", f"{dir_path}/zkDist/proof.json", "-v", f"{dir_path}/zkDist/verification.key"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # output_lines = result.stdout.split('\n')
    
    # verification_status = next((line for line in output_lines if "PASSED" in line),"FAILED")
    # if(verification_status == "FAILED"):
    #     print("Verification Failed!")
    #     return -1
    witness = []
    labels = []

    for i in range(0, len(distanceWitness)):
        if i % 2 == 0:
            witness.append(int(distanceWitness[i]))
        else:
            labels.append(int(distanceWitness[i]))

    structured_arr = np.zeros(len(witness), dtype=[('witness', np.int64), ('label', int)])

    # Populate the structured array
    structured_arr['witness'] = witness
    structured_arr['label'] = labels

    sorted_arr = np.sort(structured_arr, order='witness')
    output = np.array([str(val) for pair in sorted_arr for val in pair])

    output = output.tolist()

    # zkSortProof, sortWitness = zkSort(output, dir_path)
    # result = subprocess.run(["zokrates", "verify", "-j", f"{dir_path}/zkSort/proof.json", "-v", f"{dir_path}/zkSort/verification.key"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # output_lines = result.stdout.split('\n')
    
    # verification_status = next((line for line in output_lines if "PASSED" in line),"FAILED")
    # if(verification_status == "FAILED"):
    #     print("Verification Failed!")
    #     return -1

    # zkmaxLabelProof, prediction = zkmaxLabel(sortWitness, k, dir_path)
    # result = subprocess.run(["zokrates", "verify", "-j", f"{dir_path}/zkMaxLabel/proof.json", "-v", f"{dir_path}/zkMaxLabel/verification.key"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # output_lines = result.stdout.split('\n')
    
    # verification_status = next((line for line in output_lines if "PASSED" in line),"FAILED")
    # if(verification_status == "FAILED"):
    #     print("Verification Failed!")
    #     return -1

    # paths = ['../zkDist', '../zkSort', '../zkMaxLabel']
    # final_proof = aggregate_proofs(paths)

    # print("\nFINAL PROOF\n")
    # print(final_proof)
    
    # print(prediction)
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    print(execution_time)

if __name__ == "__main__":
    main()
