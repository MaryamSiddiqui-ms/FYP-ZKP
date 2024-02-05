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
        pred_probs = node.prediction_probs
        if X[node.feature_idx] < node.feature_val:
            # Go to the left child, assuming left child is at index (current_index * 2 + 1)
            node_index = node_index * 2 + 1
        else:
            # Go to the right child, assuming right child is at index (current_index * 2 + 2)
            node_index = node_index * 2 + 2

        # Check if the current node has no children (i.e., it's a leaf node)
        if node_index >= len(nodes):
            break

    return pred_probs


"""
    **Zero Knowledge Proof API**

        Input 1-D tree converted in array form: Array of Objects
        [
            {},{},...,{}
        ]
        Each object is a node

        Output: None

        Description:
        Tests whether the tree has been traversed properly or not

        `Assert that the function correctly implements the traversal logic, 
        moving to the left child when the feature value is less than the 
        threshold and to the right child when it's greater or equal.` 

        `Assert that the function terminates when it reaches a leaf node, i.e., a node with no children.`
"""

def zkTreeTraversal(tree, treeSize, numClasses, X_test, dir_path=''):
    
    curr_path = dir_path + '/zkTreeTraversal'
    os.chdir(curr_path)

    probs = _predict_one_sample(tree, X_test)

    data = []

    data.append(tree)
    data.append(X_test)
    data.append(probs)

    with open('input.json', 'w') as f:
        json.dump(data, f)

    with open('size.zok', 'w') as f:
        f.write('const u32 treeSize = {};\n'.format(treeSize))
        f.write('const u32 numClasses = {};\n'.format(numClasses))

    subprocess.run(["zokrates", "compile", "-i", "tree_traversal.zok", "--curve", "bls12_377"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)

    os.chdir(dir_path)
    
    return proof, probs    


if __name__ == "__main__":
    tree = [
        {},
        {},
        {},
        {},
        {},
        {},
        {}
    ]

    X_test = [1, 9, 10, 4]
    numClasses = 3
    proof, output = zkTreeTraversal(tree, len(tree), numClasses, X_test)
    print(proof)
    print(output)