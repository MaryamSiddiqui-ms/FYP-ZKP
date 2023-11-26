import sys
import pandas as pd
import os
import subprocess
import time

try:
    sys.path.append('./zkDist')
    sys.path.append('./zkSort')
    sys.path.append('./zkMaxLabel')
    
    from distance import zkDistance
    from sort import zkSort
    from maxLabel import zkmaxLabel

except Exception as e:
    print(e)


def main():
    dir_path = os.getcwd()


    df = pd.read_csv('train.csv')
    datapoint = [6,3]
    k = 3

    print(df.head(10))

    start_time = time.time()

    zkDistProof, distanceWitness = zkDistance(df, datapoint, dir_path)

    # result = subprocess.run(["zokrates", "verify", "-j", f"{dir_path}/zkDist/proof.json", "-v", f"{dir_path}/zkDist/verification.key"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # output_lines = result.stdout.split('\n')
    
    # verification_status = next((line for line in output_lines if "PASSED" in line),"FAILED")
    # if(verification_status == "FAILED"):
    #     print("Verification Failed!")
    #     return -1
    zkSortProof, sortWitness = zkSort(distanceWitness, dir_path)
    # result = subprocess.run(["zokrates", "verify", "-j", f"{dir_path}/zkSort/proof.json", "-v", f"{dir_path}/zkSort/verification.key"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # output_lines = result.stdout.split('\n')
    
    # verification_status = next((line for line in output_lines if "PASSED" in line),"FAILED")
    # if(verification_status == "FAILED"):
    #     print("Verification Failed!")
    #     return -1

    zkmaxLabelProof, prediction = zkmaxLabel(sortWitness, k, dir_path)
    # result = subprocess.run(["zokrates", "verify", "-j", f"{dir_path}/zkMaxLabel/proof.json", "-v", f"{dir_path}/zkMaxLabel/verification.key"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # output_lines = result.stdout.split('\n')
    
    # verification_status = next((line for line in output_lines if "PASSED" in line),"FAILED")
    # if(verification_status == "FAILED"):
    #     print("Verification Failed!")
    #     return -1
    
    print(prediction)
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    print(execution_time)

if __name__ == "__main__":
    main()


