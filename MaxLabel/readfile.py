# Read the content of the file
with open('output.log', 'r') as file:
    lines = file.readlines()

# Find the line containing "Witness:"
for index, line in enumerate(lines):
    if "Witness:" in line:
        # Extract the array from the next line
        array_line = lines[index + 1].strip()
        # Assuming the array is in JSON format, you can parse it
        import json
        array = json.loads(array_line)
        print(array)