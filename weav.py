import weaviate
import weaviate.classes as wvc
import os
import requests
import json

wcd_url = 'https://kuoinhivqhwekz7cc8dvia.c0.us-west3.gcp.weaviate.cloud'
wcd_api_key = 'IdvPEq93EcaKBO5IhoE0N7xPHLS9CRkrJAlF'
openai_api_key = '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'

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,                                    # Replace with your Weaviate Cloud URL
    auth_credentials=wvc.init.Auth.api_key(wcd_api_key),    # Replace with your Weaviate Cloud key
    headers={"X-OpenAI-Api-Key": openai_api_key}            # Replace with appropriate header key/value pair for the required API
)

# questions = client.collections.create(
#     name="Sentence",
#     vectorizer_config="none",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
#     generative_config=wvc.config.Configure.Generative.openai()  # Ensure the `generative-openai` module is used for generative queries
# )

data = json.loads('/Users/sam/Desktop/lebronapp/vectorized_sentences_768d.json')
print(data)# Load data

question_objs = list()
for i, d in enumerate(data):
    question_objs.append({
        "Sentence": d["sentence"],
        "Vectors": d["vector"],
    })

questions = client.collections.get("Sentences")
questions.data.insert_many(question_objs)

