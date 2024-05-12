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
import re
import tensorflow as tf
# import tf.keras.datasets.mnist as mnist
from typing import List




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
    sys.path.append('./services')

    from minMaxNormalizationAndInteger import minMaxNormalizationAndInteger
    from clean import clean_dirs
    from distance import zkDistance
    from sort import zkSort
    from maxLabel import zkmaxLabel

    from proof_composition import aggregate_proofs
    
    from decision_tree import run_dt 
    from cnn_main import generateProofCnn
    from prompt import generatePrompt

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
    
class CNNInputs(BaseModel):
    input_image: List[List[int]]


class PromptInputs(BaseModel):
    inputCode: str

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
    dir_path = os.getcwd()
    
    
    script_path = f"{dir_path}/blockchain"
    node_path = "C:\\Program Files\\nodejs\\node.exe"
    
    os.chdir(script_path)
    
    result = subprocess.run(["zokrates", "export-verifier", "-i", f"{dir_path}/{proof_path}/verification.key", "-o", f"{dir_path}/blockchain/contracts/verifier.sol"])
    

    # Construct the command to run, ensuring that newline characters are correctly escaped
    command = f'"{node_path}" -e "require(\'child_process\').exec(\'npx hardhat run scripts/deploy.js --network localhost\', (error, stdout, stderr) => {{ if (error) {{ console.error(error); return; }} console.log(stdout);}})"'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    

    # Check the result
    if result.returncode == 0:
        # Extract the address from the output
        match = re.search(r'deployed to: (0x[a-fA-F0-9]{40})', result.stdout)
        if match:
            address = match.group(1)
            print(address)
        else:
            print("Address not found in the output.")
    else:
        print(f"Command failed with return code {result.returncode}.")


        
    os.chdir(dir_path)

    with open('./blockchain/artifacts/contracts/verifier.sol/Verifier.json', 'r') as file:
        abi = json.load(file)
    
    contract_address = "0x563bAd2efacFd1C761336C4F1005CE38dc860D0A"
    
    return {"abi": abi, "contract_address": address}



@app.post("/decisiontree/prove")
def proofDT(req: DTInputs):
    clean_dirs()
    inputs = [req.x1, req.x2, req.x3, req.x4]
    
    proof, prediction = run_dt(inputs)
    
    return {
        "proof": proof,
        "prediction": prediction
    }

@app.post("/CNN/prove")
def proofCNN(req: CNNInputs):
    clean_dirs()
    dir_path = os.getcwd()
    input_image = req.input_image
    # input_image = json.loads(input_image_str)  # Convert the string back to a 2D array
    
    prediction, proof = generateProofCnn(input_image, dir_path)
    
    return {
        "proof": "proof",
        "prediction": "prediction"
    }

# @app.post("/decisiontree/verify")
# def verifyDT():
#     verification_status = verify_dt()

@app.post("/prompt-generation")
def getPrompt(req: PromptInputs):
    response = generatePrompt(req.inputCode)
    return {
        "response": response
    }


@app.get("/CNN/mnist")  
def getData():
    _, (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
    digit_images = {}    
    for image, label in zip(test_images, test_labels):
        if label not in digit_images:
            digit_images[label] = image.tolist()    
    selected_images = list(digit_images.values())    
    return selected_images

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=80)
