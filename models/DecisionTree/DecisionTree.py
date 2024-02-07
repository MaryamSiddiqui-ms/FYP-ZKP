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
    sys.path.append('./zkTreeTraversal')
    sys.path.append('./zkArgmax')
    sys.path.append('./ProofComposition')
    sys.path.append('./utils')

    
    from clean import clean_dirs

    from tree_traversal import zkTreeTraversal
    from proof_composition import aggregate_proofs

except Exception as e:
    print(e)


class DecisionTree:
    # Alishah's utils functions

    treeArr = []
    X_test = []

    _executionTime=0
    
    def run_inference():
        start_time = time.time()
        zkTreeTraversalProof, TreeTraversalWitness = zkTreeTraversal(treeArr, X_test)
        zkArgmaxProof, prediction = zkArgmax(TreeTraversalWitness)

        paths = ['../zkTreeTraversal', '../zkArgmax']
        final_proof = aggregate_proofs(paths, dir_path)

        end_time = time.time()
        _executionTime = end_time - start_time

        return prediction

    


    
