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
    