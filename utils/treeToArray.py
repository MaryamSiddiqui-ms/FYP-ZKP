import pandas as pd
import numpy as np

def treeToArray(node,arraySize):
  array = [{
                'feature_idx': 0,
                'feature_val': 0,
                'prediction_probs': np.zeros(3),
                'isLeafNode': 1
            }] * arraySize
  queue = [(node,0)]
  while queue:
    currentNode, index = queue.pop(0)
    if currentNode:
      array[index] = {
          'feature_idx': int(currentNode.feature_idx),
          'feature_val': int(currentNode.feature_val*100000000),
          'prediction_probs': [int(probs*100) for probs in currentNode.prediction_probs],
          'isLeafNode': int(bool(currentNode.left is None and currentNode.right is None))
      }
      if currentNode.left:
                queue.append((currentNode.left,  2 * index +  1))
      if currentNode.right:
                queue.append((currentNode.right,  2 * index +  2))
  return array