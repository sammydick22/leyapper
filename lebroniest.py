from analyzer import Analyzer
import requests
import weaviate
import weaviate.classes as wvc
import os
import json
from weaviate.classes.query import MetadataQuery
from weaviate.classes.query import HybridFusion
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt_tab')

class Lebroniest:
    global wcd_url
    global wcd_api_key
    global openai_api_key
    wcd_url = "https://hsr6wiuvqtggqqosyissjq.c0.us-west3.gcp.weaviate.cloud"
    wcd_api_key = "F6mO2h934DU1xET3dLk0CBg1dgyxTEMSJTjN"
    openai_api_key = "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"

    def __init__(self, transcription):
        self.transcription = transcription
        self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url=wcd_url,  # Replace with your Weaviate Cloud URL
            auth_credentials=wvc.init.Auth.api_key(
                wcd_api_key
            ),  # Replace with your Weaviate Cloud key
            headers={
                "X-OpenAI-Api-Key": openai_api_key
            },  # Replace with appropriate header key/value pair for the required API
        )


    def calculate_lebroniest(self):
        sentences = self.client.collections.get("Leyaps")
        speakers = Analyzer.extract_speakers(self.transcription)
        scores = {}

        for speaker, utterances in speakers.items():
            speaker_scores = []

            for utterance in utterances:
                # Split the utterance into sentences using nltk's sent_tokenize
                utterance_sentences = sent_tokenize(utterance)  # Tokenize the utterance into sentences
                score_sum = 0
                sentence_count = 0

                for sentence in utterance_sentences:
                    response = sentences.query.near_text(
                        query=sentence,
                        limit=5,
                        return_metadata=MetadataQuery(certainty=True),
                    )

                    splitsum = 0
                    obj_count = 0
                    for o in response.objects:
                        splitsum += o.metadata.certainty
                        obj_count += 1

                    # Ensure we're not dividing by zero
                    if obj_count > 0:
                        splitavg = splitsum / obj_count
                    else:
                        splitavg = 0

                    score_sum += splitavg  # Accumulate score for each sentence
                    sentence_count += 1  # Count the sentences

                # Calculate the average score for all sentences in the utterance
                if sentence_count > 0:
                    utterance_score = score_sum / sentence_count
                else:
                    utterance_score = 0

                speaker_scores.append(utterance_score)

            # Calculate the average score for the speaker
            if speaker_scores:
                scores[speaker] = sum(speaker_scores) / len(speaker_scores)

        lebroniest_speaker = max(scores, key=scores.get)  # Find speaker with the highest score
        print(f"Lebroniest speaker: {lebroniest_speaker}")
        print("Scores:")
        for speaker, score in scores.items():
            print(f"{speaker}: {score}")

        self.client.close()
        return {"lebroniest_speaker": lebroniest_speaker, "scores": scores}


def test_lebroniest(file_path):
    with open(file_path, "r") as file:
        transcription = file.read()
    lebroniest = Lebroniest(transcription)
    result = lebroniest.calculate_lebroniest()
    print(f"Lebroniest speaker: {result['lebroniest_speaker']}")
    print("Scores:")
    for speaker, score in result["scores"].items():
        print(f"{speaker}: {score}")


# Test the function with a sample text file
# test_lebroniest('sample.txt')
