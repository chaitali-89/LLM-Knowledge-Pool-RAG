import os
import xml.etree.ElementTree as ET
from llama_parse import LlamaParse
from config import LLAMAPARSE_API_KEY

# Initialize LlamaParse
parser = LlamaParse(
    api_key=LLAMAPARSE_API_KEY,
    result_type="markdown",  # "markdown" or "text"
    num_workers=4,
    verbose=True,
    language="en",
)

def parse_xml_to_text(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    text = ""
    for element in root.iter():
        if element.text is not None:
            text += element.text + "\n"
    return text

# Path to the directory containing XML files
xml_directory = "knowledge_pool"

# Iterate through XML files in the directory
for filename in os.listdir(xml_directory):
    if filename.endswith(".xml"):
        xml_file_path = os.path.join(xml_directory, filename)

        # Parse XML to text
        text = parse_xml_to_text(xml_file_path)

        # Save parsed text to a text file
        output_filename = os.path.splitext(filename)[0]
        output_path = os.path.join(xml_directory, f"{output_filename}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"Finished parsing {filename}")

print("Finished parsing all XML documents")
