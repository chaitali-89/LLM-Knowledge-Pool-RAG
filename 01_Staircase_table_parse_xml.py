import xml.etree.ElementTree as ET

# Path to your .xml file
file = ".\knowledge_pool\Indian Standard_ CODE OF PRACTICE FOR FIRE SAFETY OF BUILDINGS (GENERAL)_ EXIT REQUIREMENTS AND PERSONAL HAZARD.xml"

# Parse the XML file
tree = ET.parse(file)
root = tree.getroot()

# Open the output text file
with open('output.txt', 'w') as f:
    # Iterate over the elements in the XML file
    for elem in root.iter():
        # Write the element tag and text to the text file
        f.write(f"{elem.tag}: {elem.text}\n")
