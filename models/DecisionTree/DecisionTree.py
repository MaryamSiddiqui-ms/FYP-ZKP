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
    sys.path.append('../../zkTreeTraversal')
    sys.path.append('../../zkArgmax')
    sys.path.append('../../ProofComposition')
    sys.path.append('../../utils')

    # for directory in sys.path:
    #     try:
    #         file_list = os.listdir(directory)
    #         print(f"Files in {directory}: {file_list}")
    #     except FileNotFoundError:
    #         print(f"Directory not found: {directory}")
            
    from clean import clean_dirs
    from maxDepth import maxDepth
    from treeToArray import treeToArray

    from tree_traversal import zkTreeTraversal
    from proof_composition import aggregate_proofs

except Exception as e:
    print(e)


class DecisionTree:
    def __init__(self, tree, inference_point):
        self.tree = tree
        self.inference_point = inference_point
        self.execution_time = 0

    def _setExecutionTime(self, timeInSeconds):
        self._executionTime = timeInSeconds

    def getExecutionTime(self):
        return self._executionTime 


    def _preprocess(self):
        depth = maxDepth(self.tree)
        depth = (2 ** depth) - 1
        return treeToArray(self.tree, depth)
        

    def _run_inference(self, treeArr, X_test):
        start_time = time.time()
        zkTreeTraversalProof, TreeTraversalWitness = zkTreeTraversal(treeArr, X_test)
        zkArgmaxProof, prediction = zkArgmax(TreeTraversalWitness)

        paths = ['../../zkTreeTraversal', '../../zkArgmax']
        final_proof = aggregate_proofs(paths, dir_path)

        end_time = time.time()
        _setExecutionTime(end_time - start_time)

        return prediction

    def main(self):
        clean_dirs()
        treeArr = self._preprocess()
        prediction = self._run_inference(treeArr, self.inference_point)
        print("\nFINAL CLASS: ", prediction)
        print("\nEXECUTION TIME: ", self.getExecutionTime())








