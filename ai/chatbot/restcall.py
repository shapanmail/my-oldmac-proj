

from llama_index.readers.wikipedia import WikipediaReader

# Initialize WikipediaReader
reader = WikipediaReader()

# Load data from Wikipedia
documents = reader.load_data(pages=["london"])

print(documents)

