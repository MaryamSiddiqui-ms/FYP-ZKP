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
import json


current_file_path = os.path.abspath(__file__)
project_path = os.path.dirname(os.path.dirname(current_file_path))
current_pythonpath = os.environ.get('PYTHONPATH', '')
os.environ['PYTHONPATH'] = f"{project_path};{current_pythonpath}"

try:
    sys.path.append('./zkDist')
    sys.path.append('./zkSort')
    sys.path.append('./zkMaxLabel')
    sys.path.append('./zkTreeTraversal')
    sys.path.append('./zkArgmax')
    sys.path.append('./ProofComposition')
    sys.path.append('./utils')
    sys.path.append('./models/DecisionTree')
    sys.path.append('../../zkConv2D')
    sys.path.append('../../zkRelu')
    sys.path.append('../../zkSoftmax')
    sys.path.append('../../zkMaxPooling')
    sys.path.append('../../zkArgmax')
    sys.path.append('../../zkApplyWeights')
    sys.path.append('./models/CNN')

    from minMaxNormalizationAndInteger import minMaxNormalizationAndInteger
    from clean import clean_dirs
    from distance import zkDistance
    from sort import zkSort
    from maxLabel import zkmaxLabel

    from proof_composition import aggregate_proofs
    
    from decision_tree import run_dt 

except Exception as e:
    print(e)


class Item(BaseModel):
    dx: float
    dy: int
    
class DTInputs(BaseModel):
    x1: float
    x2: float
    x3: float
    x4: float

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

clean_dirs()

@app.post("/")
def KNNProof(req: Item):
    dir_path = os.getcwd()

    df = pd.read_csv('./dataset/diabetes-sub.csv')
    k = 3

    df['BMI'].loc[len(df)] = req.dx
    df['Age'].loc[len(df)] = req.dy
    df['Outcome'].loc[len(df)] = -1
 
    distances = []
    normd_df = minMaxNormalizationAndInteger(df)
    
    start_time = time.time()

    zkDistProof, distanceWitness = zkDistance(normd_df, dir_path)
    zkSortProof, sortWitness = zkSort(distanceWitness, dir_path)
    zkmaxLabelProof, prediction = zkmaxLabel(sortWitness, k, dir_path)

    paths = ['./zkDist', './zkSort']
    isVerified = aggregate_proofs(paths, dir_path)
    if not isVerified:
        raise Exception("Proofs Not Verified")
        
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    print(execution_time)

    return {
        "prediction": prediction,
        "proof": zkmaxLabelProof
    }


@app.get("/verify")
def verify(proof_path: str = ''):
    # dir_path = os.getcwd()
    # result = subprocess.run(["zokrates", "verify", "-j", f"{dir_path}/{proof_path}/proof.json", "-v", f"{dir_path}/{proof_path}/verification.key"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # output_lines = result.stdout.split('\n')
    
    # verification_status = next((line for line in output_lines if "PASSED" in line),"FAILED")
    # return {"verification_status": verification_status}

    with open('./blockchain/artifacts/contracts/verifier.sol/Verifier.json', 'r') as file:
        abi = json.load(file)
    
    contract_address = "0x1Cbb8Ee26C18AD0e193EE4CBC27F58761FC4A4a0"
    
    return {"abi": abi, "contract_address": contract_address}



@app.post("/decisiontree/prove")
def proofDT(req: DTInputs):
    clean_dirs()
    inputs = [req.x1, req.x2, req.x3, req.x4]
    
    proof, prediction = run_dt(inputs)
    
    return {
        "proof": proof,
        "prediction": prediction
    }

# @app.post("/decisiontree/verify")
# def verifyDT():
#     verification_status = verify_dt()
    

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=80)
