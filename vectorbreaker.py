import os
import json
import math

class SentenceFileSplitter:
    
    @staticmethod
    def split_into_files(vectors, output_folder, num_files=50):
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Determine how many vectors should be in each file
        vectors_per_file = math.ceil(len(vectors) / num_files)

        # Split the vector list into chunks and save each chunk as a separate file
        for i in range(num_files):
            start_index = i * vectors_per_file
            end_index = start_index + vectors_per_file
            chunk = vectors[start_index:end_index]

            # Create a file for each chunk
            output_file = os.path.join(output_folder, f'vectorized_sentences_part_{i+1}.json')
            
            with open(output_file, 'w') as file:
                json.dump(chunk, file, indent=4)
            
            print(f'Saved {len(chunk)} vectors to {output_file}')

# Example usage:
input_file = '/Users/sam/Desktop/cloudflarehacky/vectorized_sentences_768d.json'
output_folder = '/Users/sam/Desktop/cloudflarehacky/vectorchunks768'

# Load the vectorized sentences from the JSON file
with open(input_file, 'r') as file:
    vectorized_sentences = json.load(file)

# Split the vectorized sentences into 50 separate files
SentenceFileSplitter.split_into_files(vectorized_sentences, output_folder)