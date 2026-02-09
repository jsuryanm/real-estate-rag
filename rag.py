from dotenv import load_dotenv
from pathlib import Path
import os 
from uuid import uuid4

from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

CHUNK_SIZE = 1000 
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "real_estate"

llm = None 
vector_store = None 

def initialize_components():
    """
    This function webscrapes data from url and stores in vectordb
    """
    global llm,vector_store
    
    if llm is None:
        llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"),
                       model="openai/gpt-oss-120b",
                       temperature=0.9,
                       max_tokens=500)
        
    if vector_store is None:
        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code":True}
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR))

def process_urls(urls):
    '''
    This function scraps data from url 
    '''
    yield "Initializing components"
    initialize_components()

    yield "Resetting vector store"
    vector_store.reset_collection()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }


    yield "Loading data"
    loader = UnstructuredURLLoader(urls=urls,headers=headers)
    data = loader.load()

    yield "Splitting text into chunks"
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n","."," "],
        chunk_size=CHUNK_SIZE
    )

    docs = text_splitter.split_documents(data)

    yield "Add chunks to vector database"

    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs,ids=uuids)

    yield "Done adding docs to vector database"

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def generate_answer(query, debug=False):
    if not vector_store:
        raise RuntimeError("Vector database is not initialized")

    # Create retriever with more documents
    # converts the vector database as a retriever k=5 returns 5 most similar chunks question
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # Get retrieved documents for debugging
    retrieved_docs = retriever.invoke(query)
    
    if debug:
        print(f"\n=== DEBUG: Retrieved {len(retrieved_docs)} documents ===")
        for i, doc in enumerate(retrieved_docs):
            print(f"\n--- Document {i+1} ---")
            print(f"Source: {doc.metadata.get('source', 'N/A')}")
            print(f"Content preview: {doc.page_content[:300]}...")
            print()

    # Create prompt template
    template = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, say that you don't know. 
Keep the answer concise.

Context: {context}

Question: {question}

Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    # Build the RAG chain using LCEL
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Get the answer
    answer = rag_chain.invoke(query)

    # Get sources from retrieved documents
    sources = []
    for doc in retrieved_docs:
        if hasattr(doc, 'metadata') and 'source' in doc.metadata:
            source = doc.metadata['source']
            if source not in sources:
                sources.append(source)

    sources_str = ", ".join(sources) if sources else ""

    return answer, sources_str

if __name__ == "__main__":
    urls = [
        "https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html",
        "https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html"
    ]

    # Process URLs (consuming the generator)
    for status in process_urls(urls):
        print(status)

    answer, sources = generate_answer("Tell me what was the 30 year fixed mortgage rate along with the date?",debug=True)
    print(f"\nAnswer: {answer}")
    print(f"Sources: {sources}")
