from openai import OpenAI
import numpy as np
import json
from config import *

embeddings_json = "knowledge_pool\merged.json"

# Choose between "local" or "openai" mode
mode = "local"  # or "openai"
client, completion_model = api_mode(mode)

# question = "What is the program for the building?"
# question = "What is the place like?"
# question = "Is there any mention of the construction materials that should be used?"
question = "Give small description of U shaped stair?"
num_results = 10  # how many vectors to retrieve

def get_embedding(text, model=embedding_model):
    text = text.replace("\n", " ")
    response = local_client.embeddings.create(input=[text], model=model)
    vector = response.data[0].embedding
    return vector

def similarity(v1, v2):
    return np.dot(v1, v2)

def load_embeddings(embeddings_json):
    with open(embeddings_json, 'r', encoding='utf8') as infile:
        return json.load(infile)

def get_vectors(question_vector, index_lib):
    scores = []
    for vector in index_lib:
        score = similarity(question_vector, vector['vector'])
        scores.append({'content': vector['content'], 'score': score})

    scores.sort(key=lambda x: x['score'], reverse=True)
    best_vectors = scores[0:num_results]
    return best_vectors

def count_matching_words(question, pattern):
    question_words = question.lower().split()
    pattern_words = pattern.lower().split()
    matching_words = set(question_words) & set(pattern_words)
    return len(matching_words)

def rag_answer(question, prompt, model=completion_model[0]["model"], format_answer=False):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system",
             "content": prompt
             },
            {"role": "user",
             "content": question
             }
        ],
        temperature=0.1,
    )
    answer = completion.choices[0].message.content
    
    if format_answer:
        # Example patterns to identify and format answers
        patterns = (
            "spiral stair with open riser in elevation from side view",
            "split stair with straight stairs in elevation from side view",
            "straight stair in elevation from side view",
            "straight stair with landing in elevation from side view",
            "stairs in elevation from side view",
            "straight stair in elevation from side view",
            "straight stair with landing in elevation from side view",
            "stairs in U shape with 2 landings in elevation from side view",
            "stairs in Z shape with 2 landing in elevation from front view",
            "stairs in U shape with 2 landings in elevation from side view with a person climbing",
            "stairs in U shape with 2 landings in elevation from side front view and in plan with dimensions on the landing and the each stairs",
            "spiral stair with open riser viewed from plan and in elevation where there is a person standing",
            "man climbing stairs",
            "woman climbing stairs",
            "egress stairs with handrail viewed in elevation from the side from the front and in plan with detailed dimensions",
            "egress stairs without handrail viewed in elevation from the side from the front and in plan with detailed dimensions",
            "straight stair with a handrail and a man climbing up viewed in elevation viewed from the side",
            "set of technical drawings of a straight stair with dimensions viewed from the side in elevation from the front and in plan",
            "L shape stair viewed from the side in elevation",
            "set of technical drawings of a L shape stair with dimensions viewed from the side in elevation from the front and in plan",
            "straight stair with landing a handrail and a woman climbing up viewed from the side in elevation",
            "set of technical drawings of a curved stair with dimensions viewed from plan and elevations from the side and the front",
            "U shaoe curved stair without handrail with a person climbing up viewed from the side in elevation",
            "curved stair without handrail without a person climbing viewed from the side and front in elevation and plan",
            "curved stair without handrail without a person climbing viewed from the side in elevation",
            "stairs with 2 landing viewed from the side inn elevation",
            "straight stair with landing in elevation viewed from side",
            "Womb Furniture Lounge Chair with an lady silhouette sitting on it",
            "lounge chair with a man sitting on it side view",
            "Layout of a single elevator with dimensions",
            "set of 4 drawings showing an armchair from 4 different views side plan from the back and from the top",
            "set of 3 drawings with drawings of a sliding door with a glass in the middle views from the top from the front and from the side",
            "Single Hung Windows with a Springline size and scale Comparison",
            "Layout of elevators with different sizes and capacity plus having dimensions",
            "different ramp shapes Straight L-shaped and U-shaped",
            "cellar door inclined with dimensions",
            "ramp slopes for pedestrians",
            "ramp for wheel chair users slope and dimensions",
            "double sashed virtical sliding window with dimensions",
            "ramp with handrails slope and dimensions",
            "single sashed virtical sliding window with dimensions",
            "interior doors with different handle",
            "double sashed vertical sliding window with dimensions",
            "layout of elevators with different sizes",
            "single elevator layout with dimension and human silhouette",
            "window with an archtop and a rectangular bottom section with various dimensions showing the height width and height in various views the window has an arched top with a rectangular bottom section",
            "front view of a door with decorative details on it and information about it on the bottom",
            "leather office chair with different views and dimensions",
            "Layout of a single elevator",
            "simple chair with a human figure sitting on it",
            "simple chair with a human figure sitting on it",
            "ramp with handrail slope and dimensions",
            "elevators section with dimensions",
            "isolated white background"
        )
        
        # Initialize variables to track maximum similarity
        max_similarity = 0
        best_pattern = None
        
        # Check each pattern and find the one with maximum similarity
        for pattern in patterns:
            similarity_score = count_matching_words(question, pattern)
            if similarity_score > max_similarity:
                max_similarity = similarity_score
                best_pattern = pattern
        
        # If a pattern with non-zero similarity is found, format the answer
        if best_pattern:
            modified_answer = f"tchncldrwng {best_pattern}"
            return modified_answer
        
        # If no specific pattern matches, format as a generic technical drawing description
        modified_answer = f"tchncldrwng a technical drawing of {answer} isolated on a white background"
        return modified_answer
    
    else:
        return answer

# Embed our question
question_vector = get_embedding(question)

# Load the knowledge embeddings
index_lib = load_embeddings(embeddings_json)

# Retrieve the best vectors
scored_vectors = get_vectors(question_vector, index_lib)
scored_contents = [vector['content'] for vector in scored_vectors]
rag_result = "\n".join(scored_contents)

# Get answer from RAG with informed agent
prompt = f"""Answer the question based on the provided information. 
            You are given the extracted parts of a long document and a question. Provide a direct answer.
            If you don't know the answer, just say "I do not know.". Don't make up an answer.
            PROVIDED INFORMATION: {rag_result}"""

print("Prompt 1:")
print(prompt)
answer1 = rag_answer(question, prompt, format_answer=True)
print("ANSWER 1:")
print(answer1)

# Another example with a different prompt
prompt2 = f"""Provide an answer based on your understanding of the context given below.
            The question is about the specifics of the structure mentioned in the document parts.
            PROVIDED INFORMATION: {rag_result}"""

print("\nPrompt 2:")
print(prompt2)
answer2 = rag_answer(question, prompt2, format_answer=False)
print("ANSWER 2:")
print(answer2)
