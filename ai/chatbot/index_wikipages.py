# REPLACE THIS WITH YOUR CODE
import llama_index
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.program.openai import OpenAIPydanticProgram
from utils import get_apikey
from pydantic import BaseModel
import openai

from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader
from IPython.display import Markdown, display
import os
os.environ["OPENAI_API_KEY"] = get_apikey()
# define the data model in pydantic
class WikiPageList(BaseModel):
    "Data model for WikiPageList"
    pages: list # REPLACE THIS WITH YOUR CODE


def wikipage_list(query):
    openai.api_key = get_apikey()
    # REPLACE THIS WITH YOUR CODE

    prompt_template_str = """
    You are a helpful assistant. Please extract the names of the Wikipedia pages from the following request and return them as a list.
    Request: {query}
    List of Wikipedia pages:
    """
    # llm = OpenAI(api_key=get_apikey())
    program = OpenAIPydanticProgram.from_defaults(output_cls=WikiPageList, prompt_template_str=prompt_template_str, verbose=True)
    wikipage_requests = program(query=query)

    return wikipage_requests.pages


def create_wikidocs(wikipage_requests):
    reader = WikipediaReader()

    # Load data from Wikipedia pages
    documents = reader.load_data(wikipage_requests)

    return documents


def create_index(query):
    global index
    wikipage_requests = wikipage_list(query)
    documents = create_wikidocs(wikipage_requests)
    text_splits = SentenceSplitter(chunk_size=150,chunk_overlap=45)
    nodes = text_splits.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    return index

def create_index_from_html():
    # global index
    documents = SimpleWebPageReader(html_to_text=True).load_data(
        ["http://www.reece.com.au/product/showers-c458/mizu-drift-brass-overhead-shower-200mm-chrome-3-9505038"]
    )
    print(documents[0].text)
    # print("Documents loaded")
    return SummaryIndex.from_documents(documents)


#
# if __name__ == "__main__":
#     query = "/get wikipages: paris, lagos, lao"
#     index = create_index(query)
#     print("INDEX CREATED", index)

if __name__ == "__main__":
    index = create_index_from_html()
    print("INDEX CREATED", index)
    # set Logging to DEBUG for more detailed outputs
    query_engine = index.as_query_engine()
    query1 = "Tell me about mizu brand"
    query2 = "what is the price of Mizu Drift Brass Overhead Shower 200mm Chrome"
    query3 = "Give me a summary of Mizu Drift specification"
    query4 = "Can I use this Mizu brass in my toilet"

    print( query_engine.query(query1))
    print( query_engine.query(query2))
    print( query_engine.query(query3))
    print( query_engine.query(query4))
    # display(Markdown(f"{response}"))


