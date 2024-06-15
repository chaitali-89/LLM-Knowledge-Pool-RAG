import json
import os

def validate_json_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding='utf-8') as file:
                    json.load(file)
                print(f"{filename} is valid.")
            except json.JSONDecodeError as e:
                print(f"{filename} is not valid JSON. Error: {e}")
            except UnicodeDecodeError as e:
                print(f"{filename} has encoding issues. Error: {e}")

# Validate JSON files
validate_json_files("knowledge_pool")
