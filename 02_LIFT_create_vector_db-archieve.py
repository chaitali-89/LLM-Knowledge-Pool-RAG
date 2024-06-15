import json
import os
from config import *

document_to_embed = "knowledge_pool/Indian Standard_ CODE OF PRACTICE FOR FIRE SAFETY OF BUILDINGS (GENERAL)_ EXIT REQUIREMENTS AND PERSONAL HAZARD.txt"

def get_embedding(text, model=embedding_model):
   text = text.replace("\n", " ")
   return local_client.embeddings.create(input = [text], model=model).data[0].embedding

# Read the text document
with open(document_to_embed, 'r', encoding='utf-8', errors='ignore') as infile:
    text_file = infile.read()

# Split the text into sections based on titles and subtitles
chunks = []
current_chunk = ""
for line in text_file.split("\n"):
    if line.startswith("#"):  # This is a title or subtitle
        if current_chunk:  # Save the previous chunk if it exists
            chunks.append(current_chunk)
        current_chunk = line  # Start a new chunk with the title
    else:
        current_chunk += "\n\n" + line  # Add to the current chunk

if current_chunk:  # Don't forget the last chunk
    chunks.append(current_chunk)

# Prepending "Indian Standard" to each chunk
chunks = ["Indian Standard: " + chunk for chunk in chunks]
        
# Create the embeddings
embeddings = []
for i, chunk in enumerate(chunks):
    print(f'{i} / {len(chunks)}')
    vector = get_embedding(chunk.encode(encoding='utf-8').decode())
    database = {'content': chunk, 'vector': vector}
    embeddings.append(database)

# Save the embeddings to a json file
output_filename = os.path.splitext(document_to_embed)[0]
output_path = f"{output_filename}.json"

with open(output_path, 'w', encoding='utf-8') as outfile:
    json.dump(embeddings, outfile, indent=2, ensure_ascii=False)

print(f"Finished vectorizing. Created {output_path}")
