import assemblyai as aai
import os

class Transcriber:
    def __init__(self):
        # Set your API key for AssemblyAI
        aai.settings.api_key = "2cdae29828b643d38981c70e4b8147d6"

    def transcribe(self, FILE_URL):
        # Set the transcription config with speaker labels enabled
        config = aai.TranscriptionConfig(speaker_labels=True)
        transcriber = aai.Transcriber()

        # Perform transcription
        transcript = transcriber.transcribe(FILE_URL, config=config)

        # Return the transcription as a string
        transcription_string = ""
        for utterance in transcript.utterances:
            transcription_string += f"Speaker {utterance.speaker}: {utterance.text}\n"
        print(transcription_string)
        return transcription_string

        # Generate file name from the URL
    def save_transcription(transcript, FILE_URL):
        file_name = FILE_URL.split('/')[-1].split('.')[0]
        output_folder = 'TXTs'

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save the transcription to a .txt file
        output_path = os.path.join(output_folder, f"{file_name}.txt")
        with open(output_path, "w") as f:
            for utterance in transcript.utterances:
                f.write(f"Speaker {utterance.speaker}: {utterance.text}\n")
            print(f"Transcription saved to {output_path}")

        # Return the file path
        return output_path

