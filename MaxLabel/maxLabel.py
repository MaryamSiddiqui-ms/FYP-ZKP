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
        result = subprocess.run(["zokrates", "compute-witness", "--verbose", "-a"] + labels, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_lines = result.stdout.split('\n')
        witness_line = next((line for line in output_lines if "Witness:" in line), None)
        if witness_line:
            witness_index = output_lines.index(witness_line)
            witness_array_line = output_lines[witness_index + 1]
            print( witness_array_line ) 
        else:
            print("Witness not found in the output.")
        with open('witness_output.log', 'w') as output_file:
            output_file.write( witness_array_line )
            
        subprocess.run(["zokrates", "generate-proof"])
        with open("proof.json", 'r') as proof_file:
            proof = json.load(proof_file)
            
        with open('witness_output.log', 'r') as file:
            content = json.load(file)
            print("Prediction: ", content[0])

# Assuming that the size is 5
# k=3

zkmaxLabel(3)
