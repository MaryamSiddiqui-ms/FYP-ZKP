import pandas as pd
import numpy as np

def maxDepth(node):
  # print(node is None)
  if node is None:
    return 0
  else:
    left = maxDepth(node.left)
    right = maxDepth(node.right)
    return max(left,right)+1
