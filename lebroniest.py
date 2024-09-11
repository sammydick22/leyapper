from analyzer import Analyzer
import requests

class Lebroniest:
    def __init__(self, transcription):
        self.transcription = transcription

    def calculate_lebroniest(self):
        speakers = Analyzer.extract_speakers(self.transcription)
        scores = {}
        for speaker, utterances in speakers.items():
            speaker_scores = []
            for utterance in utterances:
                response = requests.get(f"https://vector-database.kevin-taylor1924.workers.dev/query?query={utterance}")
                response_json = response.json()
                if response_json["matches"]["count"] > 0:
                    speaker_scores.append(response_json["matches"]["matches"][0]["score"])
            if speaker_scores:
                scores[speaker] = sum(speaker_scores) / len(speaker_scores)
        lebroniest_speaker = max(scores, key=scores.get)
        print(f"Lebroniest speaker: {lebroniest_speaker}")
        print("Scores:")
        for speaker, score in scores.items():
            print(f"{speaker}: {score}")

        return {"lebroniest_speaker": lebroniest_speaker, "scores": scores}

def test_lebroniest(file_path):
    with open(file_path, 'r') as file:
        transcription = file.read()
    lebroniest = Lebroniest(transcription)
    result = lebroniest.calculate_lebroniest()
    print(f"Lebroniest speaker: {result['lebroniest_speaker']}")
    print("Scores:")
    for speaker, score in result["scores"].items():
        print(f"{speaker}: {score}")

# Test the function with a sample text file
# test_lebroniest('sample.txt')
