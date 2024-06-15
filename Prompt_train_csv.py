import csv

# Initialize an empty list to store patterns
patterns = []

# Replace '.\knowledge_pool\metadata.csv' with the path to your actual CSV file
csv_file_path = '.\knowledge_pool\metadata.csv'

try:
    with open(csv_file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        
        # Skip the header if present
        headers = next(csv_reader, None)
        
        for row in csv_reader:
            if len(row) >= 2:  # Ensure each row has at least two columns
                filename = row[0].strip()  # Assuming the filename is in the first column
                description = row[1].strip()  # Assuming the description is in the second column
                
                # Process the description to extract the pattern
                pattern = description.replace('tchncldrwng ', '').replace(' isolated on a white background', '')
                
                # Append the cleaned pattern to the list
                patterns.append(pattern)
            else:
                print(f"Ignoring row with insufficient data: {row}")
except FileNotFoundError:
    print(f"File '{csv_file_path}' not found.")
except Exception as e:
    print(f"Error occurred: {str(e)}")

# Convert the list of patterns to a tuple
patterns_tuple = tuple(patterns)

print(patterns_tuple)
