import subprocess 
import json


def zkmaxLabel(size):
# Extract the labels from the KNN output
        with open('maxLabel.json', 'r') as f:
            knn_output = json.load(f)
        # label = [item[-1] for item in knn_output]
        label = knn_output[1::2]
        # Convert the labels to strings and join them with commas
        # labels_str = ','.join(map(str, labels))
        labels = list(map(str, label))
        print(labels)

        # Run the Zokrates program with the labels as input
        subprocess.run(["zokrates", "compile", "-i", "maxLabel.zok"])
        subprocess.run(["zokrates", "setup"])
        with open('output.log', 'w') as output_file:
            subprocess.run(["zokrates", "compute-witness","--verbose", "-a"]+labels,stdout=output_file,stderr=subprocess.PIPE)      # Generate the proof
        subprocess.run(["zokrates", "generate-proof"])
        with open("proof.json", 'r') as proof_file:
            proof = json.load(proof_file)
        print(proof)

# Assuming that the size is 5
# k=3

zkmaxLabel(3)
