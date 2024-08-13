#checker.py tells you which books and chapters do not start with two new line characters
import os

# Path to the directory containing the folders and files
base_dir = 'bom2/bom-english'

# List to store files that don't start with two newlines
files_without_newlines = []

# Iterate through all files in the directory
for root, dirs, files in os.walk(base_dir):
    for file in files:
        file_path = os.path.join(root, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read the first few characters
            start_content = f.read(2)
            # Check if the first two characters are newline characters
            if start_content != '\n\n':
                files_without_newlines.append(file_path)

# Print the results
if files_without_newlines:
    print("Files that don't start with two newline characters:")
    for file in files_without_newlines:
        print(file)
else:
    print("All files start with two newline characters.")



"""
bom2/bom-english/moroni/9.txt
bom2/bom-english/helaman/7.txt
bom2/bom-english/helaman/13.txt
bom2/bom-english/helaman/1.txt
bom2/bom-english/alma/7.txt
bom2/bom-english/alma/36.txt
bom2/bom-english/alma/5.txt
bom2/bom-english/alma/45.txt
bom2/bom-english/alma/39.txt
bom2/bom-english/alma/38.txt
bom2/bom-english/alma/21.txt
bom2/bom-english/alma/9.txt
bom2/bom-english/alma/17.txt
bom2/bom-english/mosiah/9.txt
bom2/bom-english/mosiah/23.txt
bom2/bom-english/mosiah/1.txt
bom2/bom-english/3-nephi/11.txt
the end at moroni 10
"""