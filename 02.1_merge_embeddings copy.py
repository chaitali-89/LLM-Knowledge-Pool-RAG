import json
import os

def merge_json_files(directory):
    merged_data = list()
    for filename in os.listdir(directory):
        if filename.endswith(".json") and filename != "merged.json":
            file_path = os.path.join(directory, filename)
            # Ensure UTF-8 encoding is specified when reading files
            with open(file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                merged_data.extend(data)
    return merged_data

# Merge JSON files
merged_json = merge_json_files("knowledge_pool")

output_file_path = "knowledge_pool/merged.json"

# Ensure UTF-8 encoding is specified when writing files
with open(output_file_path, "w", encoding='utf-8') as output_file:
    json.dump(merged_json, output_file, indent=4)

print(f"Merged JSON saved to {output_file_path}")



