from sentence_transformers import SentenceTransformer
import numpy as np

# Model selection
model_name = "all-MiniLM-L6-v2"  # You can choose other models if desired
model = SentenceTransformer(model_name)

# Function to generate vectors
def generate_vectors(texts, model=model):
    """Generate semantic vectors for a list of texts."""
    return model.encode(texts, convert_to_numpy=True)

def return_vectors(texts):
    # Generate vectors
    text_vectors = generate_vectors(texts, model)   
    # Display generated vectors
    for i, vec in enumerate(text_vectors):
        print(f"Text {i}: {texts[i]}")
        print(f"Vector {i}: {vec[:5]}... (dim: {len(vec)})")
