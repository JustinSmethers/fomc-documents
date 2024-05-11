from scraping.scrape_statements import scrape_statements
from extraction.extract_text import get_text_from_pdf
from vectorization.vectorize_text import generate_vectors
from vectorization.vector_search import vector_search

def main():
    # Scrape the statements
    print('Scraping statements...')
    pdf_path = scrape_statements()
    print('Statements scraped')
    print(f'PDF Path: {pdf_path}')

    # Extract text from the PDF
    print(f'Extracting text from {pdf_path}...')
    extracted_text = get_text_from_pdf(pdf_path)
    print('Text extracted')
    # print(f"Extracted Text:\n{extracted_text}")
    sentence_list = extracted_text.split('.')
    # print(f"Sentence List:\n{sentence_list}")

    # Generate vectors for the text
    print('Generating vectors...')
    text_vectors = generate_vectors(sentence_list)
    print('Vectors generated')
    # Generate a constant list of page_nums and doc_ids
    page_nums = [1] * len(sentence_list)
    doc_ids = [1] * len(sentence_list)

    # Vector search for a specific word
    search_word = 'inflation'

    # Perform vector search
    print(f'Searching for "{search_word}"...')
    search_results = vector_search(doc_ids, page_nums, text_vectors, sentence_list, search_word, len(sentence_list))
    print('Search complete')

    # Display search results 
    for result in search_results:
        print(f'score: {result[1]} \t{result[0][:120]}')

    
if __name__ == '__main__':
    main()
