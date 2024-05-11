# FOMC Press Release Sentiment Analysis

## Overview
This project is aiming to scrape FOMC press releases from the Federal Reserve website and analyze the sentiment of the press releases. The project will also include a simple analysis of the sentiment of the press releases over time. The hope is to get meaningful insights into how the Federal Reserve is viewing inflation and the economy over time, mostly just out of curiosity.


## Setup
I'm using Python 3.12.1 on my local machine. The project includes a `requirements.txt` file that lists the required packages. To install the required packages, run the following command:

>```pip install -r requirements.txt```

To run the project as-is:

>```python3 main.py```

## Current Status
Running `main.py` downloads the press release from May 2024, extracts the text from the PDF, and vectorizes the text.  The script then stores the embeddings in an in-memory DuckDB database and performs a vector search on the text to find the most similar press release to the word 'inflation'.

## Todo
- Create a Dockerfile to run the project in a container.
- Analyze the sentiment of the press releases.
- Analyze the rest of the press releases from 2024.
- Analyze the sentiment of the press releases over time.
- Add tests.
- Add in key word analysis or something else to make the analysis more interesting.

## Structure
The project is structured as follows:
- `data/`: Contains the data collected from the Federal Reserve website.

## Improvements
The project can be improved in the following ways:
- `scraping/`: The scraping code currrently only downloads press releases from 2024. The code can be improved to download press releases from other years.
- `extraction/`: The code for extracting the text from the PDFs can be improved to better clean the text. Right now, There are special characters in the text that are not being removed. The script returns a list of sentesnces, but you might explore other ways to extract the text, or prune the list of sentences further.
- `vectorization/`: The code for vectorizing the text can be improved. The current code uses a simple model. You might explore different models or hyperparameters. The vector search uses DuckDB to store the vectors, which only supports vector search in in-memory databases. The code could eventually persist the embeddings to disk once DuckDB supoorts it. See documentation [here](https://duckdb.org/docs/extensions/vss).
- `tests/`: There are no tests.
- `main.py`: The main script could be more sophisticated.
- `Dockerfile`: Need to create a Dockerfile to run the project in a container.

## Data Collection
The data will be collected by scraping the FOMC press releases from the Federal Reserve website. The data will be collected in two steps. First, the links to the press releases will be collected from the FOMC press release page. Second, the text of the press releases will be collected from the individual press release PDFs.

