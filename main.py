import sys
import pandas as pd
import os
import subprocess
import time
import numpy as np
import uvicorn
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

current_file_path = os.path.abspath(__file__)
project_path = os.path.dirname(os.path.dirname(current_file_path))
current_pythonpath = os.environ.get('PYTHONPATH', '')
os.environ['PYTHONPATH'] = f"{project_path};{current_pythonpath}"

try:
    sys.path.append('./zkDist')
    sys.path.append('./zkSort')
    sys.path.append('./zkMaxLabel')
    sys.path.append('./ProofComposition')
    sys.path.append('./utils')

    from minMaxNormalizationAndInteger import minMaxNormalizationAndInteger
    from clean import clean_dirs
    from distance import zkDistance
    from sort import zkSort
    from maxLabel import zkmaxLabel

    from proof_composition import aggregate_proofs

except Exception as e:
    print(e)


class Item(BaseModel):
    dx: float
    dy: int

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
clean_dirs()
@app.post("/")
def main(req: Item):
    dir_path = os.getcwd()

    df = pd.read_csv('./dataset/diabetes-sub.csv')
    k = 3

    # datapoint = [req.dx, req.dy]
    # datapoint.append(-1)
    # df.loc[len(df)] = datapoint

    df['BMI'].loc[len(df)] = req.dx
    df['Age'].loc[len(df)] = req.dy
    df['Outcome'].loc[len(df)] = -1
 
    distances = []
    normd_df = minMaxNormalizationAndInteger(df)
    # print(datapoint)
    
    start_time = time.time()

    zkDistProof, distanceWitness = zkDistance(normd_df, dir_path)
    zkSortProof, sortWitness = zkSort(distanceWitness, dir_path)
    zkmaxLabelProof, prediction = zkmaxLabel(sortWitness, k, dir_path)

    paths = ['../zkDist', '../zkSort', '../zkMaxLabel']
    final_proof = aggregate_proofs(paths, dir_path)

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    print(execution_time)

    return {
        "prediction": prediction,
        "proof": final_proof
    }


@app.get("/verify")
def verify():
    dir_path = os.getcwd()
    result = subprocess.run(["zokrates", "verify", "-j", f"{dir_path}/ProofComposition/proof.json", "-v", f"{dir_path}/ProofComposition/verification.key"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_lines = result.stdout.split('\n')
    
    verification_status = next((line for line in output_lines if "PASSED" in line),"FAILED")
    return {"verification_status": verification_status}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=80)
