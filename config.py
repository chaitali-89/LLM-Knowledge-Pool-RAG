import random
from openai import OpenAI
from keys import *


# API
local_client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Models
embedding_model = "nomic-ai/nomic-embed-text-v1.5-GGUF"
#embedding_model = "gaianet/Nomic-embed-text-v1.5-Embedding-GGUF"
#embedding_model = "second-state/Nomic-embed-text-v1.5-Embedding-GGUF"

mermaid = [
        {
            "model": "afrideva/Mermaid-Llama-6.7B-RAG-Code-Instruct-GGUF",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
        }
]

phi3 = [
        {
            "model": "afrideva/Phi-3-Context-Obedient-RAG-GGUF",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
            "cache_seed": random.randint(0, 100000),
        }
]


mistral_7b = [
        {
            "model": "RichardErkhov/h2oai_-_h2ogpt-gm-7b-mistral-chat-sft-dpo-rag-v1-gguf",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
        }
]

bartowski = [
        {
            "model": "bartowski/Phi-3-Context-Obedient-RAG-GGUF",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
        }
]

mistral_7b1 = [
        {
            "model": "RichardErkhov/h2oai_-_h2ogpt-gm-7b-mistral-chat-sft-dpo-rag-v1-gguf",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
            "cache_seed": random.randint(0, 100000),
        }
]

# Notice how this model is not running locally. It uses an OpenAI key.
gpt4_turbo = [
        {
            "model": "gpt-4-turbo-preview",
            "api_key": OPENAI_API_KEY,
            "cache_seed": random.randint(0, 100000),
        }
]

phi31 = [
        {
            "model": "bartowski/Phi-3-Context-Obedient-RAG-GGUF",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
            "cache_seed": random.randint(0, 100000),
        }
]

# llama3 = [
#         {
#             "model": "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
#             'api_key': 'any string here is fine',
#             'api_type': 'openai',
#             'base_url': "http://localhost:1234/v1",
#             "cache_seed": random.randint(0, 100000),
#         }
# ]

#If you download any new models, make sure to add its configuration here. Simply change the "model" name to the correct one.
Mistral_7B_32k = [
        {
            "model": "TheBloke/SciPhi-Self-RAG-Mistral-7B-32k-GGUF",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
            "cache_seed": random.randint(0, 100000),
        }
]

# Helping function
def api_mode(mode):
    if mode == "local":
        client = local_client
        completion_model = phi3  # Whatever model you want to use locally
        return client, completion_model
    elif mode == "openai":
        client = openai_client
        completion_model = gpt4_turbo
        return client, completion_model
    else:
        raise ValueError("Please specify if you want to run local or openai models")