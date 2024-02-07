import numpy as np
import subprocess 
import json
import os
import sys

def _predict_one_sample(nodes, X: np.array) -> np.array:
    """Returns prediction for 1 dim array"""
    # Assuming the root node is at index 0
    node_index = 0

    while True:
        node = nodes[node_index]
        pred_probs = node["prediction_probs"]
        if X[node["feature_idx"]] < node["feature_val"]:
            node_index = node_index * 2 + 1
        else:
            node_index = node_index * 2 + 2

        if node_index >= len(nodes) or node["isLeafNode"]:
            break

    return pred_probs

def zkTreeTraversal(tree, treeSize, numClasses, num_features, X_test, dir_path=''):
    
    # curr_path = dir_path + '/zkTreeTraversal'
    # os.chdir(curr_path)

    probs = _predict_one_sample(tree, X_test)

    data = []

    probs = [str(i) for i in probs]
    X_test = [str(i) for i in X_test]
    tree = [
        {
            "feature_idx": str(node["feature_idx"]),
            "feature_val": str(node["feature_val"]),
            "prediction_probs": [str(prob) for prob in node["prediction_probs"]],
            "isLeafNode": node["isLeafNode"]
        }
        for node in tree
    ]

    data.append(tree)
    data.append(X_test)
    data.append(probs)

    with open('input.json', 'w') as f:
        json.dump(data, f)

    with open('size.zok', 'w') as f:
        f.write('const u32 treeSize = {};\n'.format(treeSize))
        f.write('const u32 numClasses = {};\n'.format(numClasses))
        f.write('const u32 numFeatures = {};\n'.format(num_features))

    subprocess.run(["zokrates", "compile", "-i", "tree_traversal.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])

    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)

    # os.chdir(dir_path)
    return proof, probs    


# if __name__ == "__main__":
#     tree = [
#         {
#             "feature_idx": 1,
#             "feature_val": 500,
#             "prediction_probs": [54, 23, 10],
#             "isLeafNode": False
#         },
#         {
#             "feature_idx": 1,
#             "feature_val": 500,
#             "prediction_probs": [54, 23, 10],
#             "isLeafNode": True
#         },
#         {
#             "feature_idx": 1,
#             "feature_val": 500,
#             "prediction_probs": [54, 23, 10],
#             "isLeafNode": False
#         },
#         {
#             "feature_idx": 0,
#             "feature_val": 0,
#             "prediction_probs": [0, 0, 0],
#             "isLeafNode": True
#         },
#         {
#             "feature_idx": 0,
#             "feature_val": 0,
#             "prediction_probs": [0, 0, 0],
#             "isLeafNode": True
#         },
#         {
#             "feature_idx": 1,
#             "feature_val": 500,
#             "prediction_probs": [54, 23, 10],
#             "isLeafNode": True
#         },
#         {
#             "feature_idx": 1,
#             "feature_val": 500,
#             "prediction_probs": [54, 23, 10],
#             "isLeafNode": True
#         }
#     ]

#     X_test = [1, 9, 10, 4]
    
#     numClasses = 3
#     num_features = 4
#     proof, output = zkTreeTraversal(tree, len(tree), numClasses, num_features, X_test)
#     # print(proof)
#     print("OUTPUT FROM PYTHON: ", output)
    