from sentence_transformers import SentenceTransformer
import json

class SentenceVectorizer768:
    @staticmethod
    def load_sentences_from_json(input_file):
        # Load sentences from a JSON file
        with open(input_file, 'r') as json_file:
            sentences = json.load(json_file)
        return sentences

    @staticmethod
    def vectorize_sentences(sentences):
        # Load the model that generates 768-dimensional embeddings
        model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        
        # Generate embeddings for each sentence
        sentence_vectors = []
        for sentence in sentences:
            if sentence.strip():  # Skip empty sentences
                embedding = model.encode(sentence)
                sentence_vectors.append({
                    "sentence": sentence,
                    "vector": embedding.tolist()
                })
                print(f"Vectorized: {sentence}")
        
        return sentence_vectors

    @staticmethod
    def save_vectors_to_json(vectors, output_file):
        # Save the sentence vectors to a JSON file
        with open(output_file, 'w') as json_file:
            json.dump(vectors, json_file, indent=4)
        print(f"Vectorized sentences saved to {output_file}")

# Example usage:
input_file = '/Users/sam/Desktop/cloudflarehacky/giant_training_data.json'
output_file = 'vectorized_sentences_768d.json'

# Load sentences
sentence_list = SentenceVectorizer768.load_sentences_from_json(input_file)

# Vectorize the sentences (768 dimensions)
vectorized_sentences = SentenceVectorizer768.vectorize_sentences(sentence_list)

# Save the vectorized sentences to a JSON file
SentenceVectorizer768.save_vectors_to_json(vectorized_sentences, output_file)