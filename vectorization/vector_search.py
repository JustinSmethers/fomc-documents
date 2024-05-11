import duckdb
from sentence_transformers import SentenceTransformer
from vectorization.vectorize_text import generate_vectors
from db.db_setup import initialize_db

# Initialize DuckDB connection
con = initialize_db()

# Create an HNSW index on the vector column
def create_index():
    con.execute("""
        CREATE INDEX IF NOT EXISTS idx
        ON embeddings
        USING HNSW (vec)
        WITH (metric='cosine');
    """)

# Function to add new vectors
def add_vectors_to_db(doc_ids, page_nums, text_vectors, sentences):
    for doc_id, page_num, vec, sentence in zip(doc_ids, page_nums, text_vectors, sentences):
        con.execute("INSERT INTO embeddings VALUES (?, ?, ?, ?)", (doc_id, page_num, vec.tolist(), sentence))
    create_index()

# Function to perform similarity search
def search_similar_vectors(query, k):
    query_vector = generate_vectors([query])[0]
    results = con.execute("""
        SELECT doc_id, page_num, sentence, array_cosine_similarity(vec, ?::FLOAT[384]) AS similarity
        FROM embeddings
        ORDER BY similarity DESC
        LIMIT ?
    """, (query_vector.tolist(), k)).fetchall()
    return results

# Function to sort search results by similarity score
def sort_results(results):
    # Return the first 30 characters of the sentence and the similarity score rounded to 4 decimal places
    pruned_results = [(result[2], round(result[3], 4)) for result in results]

    # Sort the results by similarity score
    sorted_results = sorted(pruned_results, key=lambda x: x[1], reverse=True)

    return sorted_results
    

def vector_search(doc_ids, page_nums, text_vectors, sentences, query, k=3):
    # Add vectors to the database
    add_vectors_to_db(doc_ids, page_nums, text_vectors, sentences)
    
    # Perform similarity search
    search_results = search_similar_vectors(query, k)
    sorted_search_results = sort_results(search_results)
    
    return sorted_search_results
