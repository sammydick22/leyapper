import os
from cerebras.cloud.sdk import Cerebras, BadRequestError
import openai

class Analyzer:
    
    @staticmethod
    def clean_file(path):
        # Initialize the Cerebras client
        client = Cerebras(
            api_key="csk-r23d9tddj8rnne53wtxvhfmvv4ttmeckrww4h8enmpyxcddd"
        )

        # Path to the trimmed_txts folder
        output_folder = '/Users/sam/Desktop/cloudflarehacky/trimmed_txts/'

        # Get all .txt files from the folder
        txt_files = [f for f in os.listdir(path) if f.endswith('.txt')]

        # Process each .txt file in the folder
        for txt_file in txt_files:
            file_path = os.path.join(path, txt_file)

            # Create the cleaned file name by replacing spaces with underscores and appending '_cleaned'
            base_filename = os.path.splitext(txt_file)[0]  # Get the file name without the extension
            cleaned_filename = f"{base_filename.replace(' ', '_')}_cleaned.txt"
            cleaned_file_path = os.path.join(output_folder, cleaned_filename)

            # Open and read the contents of the current .txt file
            with open(file_path, 'r') as file:
                file_content = file.read().strip()  # Read the entire content and remove leading/trailing whitespace
                
                if not file_content:
                    continue  # Skip empty files
                
                try:
                    # Send the file content to the Cerebras API
                    completion_create_response = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "Return the letter of the speaker that is Lebron James speaking (he usually will be the one being interviewed) (Speaker A, Speaker B, etc). Make sure Lebron James is speaking, not being adressed. Just return the letter. Nothing else."
                            },
                            {
                                "role": "user",
                                "content": file_content  # Use the content of the current file
                            }
                        ],
                        model="llama3.1-8b",
                        stream=False,
                        max_tokens=8192,
                        temperature=0,
                        top_p=0,
                        seed=5
                    )

                    # Extract the letter from the response
                    speaker_letter = completion_create_response.choices[0].message.content.strip()

                    if speaker_letter == 'Z':
                        # Clear the content of the file if multiple speakers (Z) are detected
                        with open(file_path, 'w') as f:
                            f.write('')  # Overwrite the file with an empty string
                        print(f"Multiple speakers detected in {txt_file}. File content cleared.")
                        continue

                    # Keep only the content from the identified speaker
                    cleaned_content = Analyzer.extract_speaker_content(file_content, speaker_letter)

                    # Write the cleaned content to the new cleaned file in the trimmed_txts folder
                    with open(cleaned_file_path, 'a') as output_file:
                        output_file.write(cleaned_content + '\n')

                    print(f"Processed {txt_file}: Speaker {speaker_letter}'s content saved to {cleaned_filename} in trimmed_txts folder.")

                except BadRequestError as e:
                    # Check if it's the token limit error and skip this file
                    if 'context_length_exceeded' in str(e):
                        print(f"Skipped {txt_file}: Content exceeded token limit.")
                    else:
                        print(f"Error processing {txt_file}: {e}")

    @staticmethod
    def extract_speaker_content(content, speaker_letter):
        """
        Extracts lines that start with the specified speaker letter (e.g., "Speaker B:").
        Removes the speaker label and keeps only the relevant speaker's content.
        """
        cleaned_lines = []
        lines = content.splitlines()
        speaker_tag = f"Speaker {speaker_letter}:"
        
        for line in lines:
            if line.startswith(speaker_tag):
                # Remove 'Speaker X:' and keep the rest of the line
                cleaned_lines.append(line.replace(speaker_tag, "").strip())
        
        # Join the cleaned lines into a single string
        return '\n\n'.join(cleaned_lines)


    def extract_speakers(transcription):
        speakers = {}
        lines = transcription.splitlines()
        for line in lines:
            if line.startswith('Speaker'):
                speaker, text = line.split(': ', 1)
                speaker = speaker.split(' ')[1]  # Extract the speaker letter (e.g., 'A', 'B', etc.)
                if speaker not in speakers:
                    speakers[speaker] = []
                speakers[speaker].append(text)
        return speakers
