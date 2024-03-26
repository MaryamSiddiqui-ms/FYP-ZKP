import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API")


genai.configure(api_key=api_key)

generation_config = {
  "temperature": 0.05,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

prompt_parts = [
  "Identify if any of the following computations are being performed in the code: Sorting, Distance, Relu, Softmax, TreeTraversal, Argmax, MaxLabel, Convolution, MaxPooling, ApplyWeights. For each computation identified, add a comment specifying the checkpoint. Use the appropriate function calls and provide the necessary output variables as indicated",
  "input: def traverse(self, node, X):        while node:            pred_probs = node.prediction_probs            if X[node.feature_idx] < node.feature_val:                node = node.left            else:                node = node.right        return pred_probs    def _predict_one_sample(self, X: np.array) -> np.array:        node = self.tree        pred _probs = traverse(node, X)    def predict(self, X_set: np.array) -> np.array:        pred_probs = self.predict_proba(X_set)        preds = np.argmax(pred_probs, axis=1)        return preds",
  "output: ```python\ndef traverse(self, node, X):\n    while node:\n        pred_probs = node.prediction_probs\n        if X[node.feature_idx] < node.feature_val:\n            node = node.left\n        else:\n            node = node.right\n    return pred_probs\n\ndef _predict_one_sample(self, X: np.array) -> np.array:\n    node = self.tree\n    # Checkpoint #1: TreeTraversal\n    # zkTreeTraversal(node, X) -> pred_probs, proofOfTreeTraversal \n    pred _probs = traverse(node, X)\n\ndef predict(self, X_set: np.array) -> np.array:\n    pred_probs = self.predict_proba(X_set)\n    # Checkpoint #2: Argmax\n    # zkArgmax(pred_probs) -> preds, proofOfArgmax\n    preds = np.argmax(pred_probs, axis=1)\n    return preds\n```",
  "input: def euclidean_distance(row1, row2):    distance = 0.0    for i in range(len(row1)-1):        distance += (row1[i] - row2[i])**2    return sqrt(distance)def get_neighbors(train, test_row, num_neighbors):    distances = list()    for train_row in train:        dist = euclidean_distance(test_row, train_row)        distances.append((train_row, dist))        distances.sort(key=lambda tup: tup[1])    neighbors = list()    for i in range(num_neighbors):        neighbors.append(distances[i][0])    return neighborsdef predict_classification(train, test_row, num_neighbors):    neighbors = get_neighbors(train, test_row, num_neighbors)    output_values = [row[-1] for row in neighbors]    prediction = max(set(output_values), key=output_values.count)    return prediction",
  "output: ```python\ndef euclidean_distance(row1, row2):\n    distance = 0.0\n    for i in range(len(row1)-1):\n        distance += (row1[i] - row2[i])**2\n    return sqrt(distance)\n\ndef get_neighbors(train, test_row, num_neighbors):\n    distances = list()\n    for train_row in train:\n        # Checkpoint #1: Distance Computation\n        # zkDist(test_row, train_row) -> dist, proofOfDistance\n        dist = euclidean_distance(test_row, train_row)\n        distances.append((train_row, dist))\n        # Checkpoint #2: Sort Computation\n        # zkSort(distances) -> sortedDistances, proofOfSort\n        distances.sort(key=lambda tup: tup[1])\n    neighbors = list()\n    for i in range(num_neighbors):\n        neighbors.append(distances[i][0])\n    return neighbors\n\ndef predict_classification(train, test_row, num_neighbors):\n    neighbors = get_neighbors(train, test_row, num_neighbors)\n    output_values = [row[-1] for row in neighbors]\n    # Checkpoint #3: MaxLabel\n    # zkMaxLabel(output_values) -> prediction, proofOfMaxLabel\n    prediction = max(set(output_values), key=output_values.count)\n    return prediction\n```",
]

def generatePrompt(inputs):
    parsedInput = "input: " + inputs
    prompt_parts.append(parsedInput)
    output = "output: "
    prompt_parts.append(output)
    
    response = model.generate_content(prompt_parts)
    return response.text
    
    
