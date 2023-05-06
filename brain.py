import os

import pinecone
from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.schema import Document
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings


def ingest_rules(url: str) -> list[Document]:
    """Ingest the rules PDF document into the Vector DB"""
    loader = PyMuPDFLoader(url)
    docs = loader.load()
    for doc in docs:
        doc.metadata = {
            'page_number': str(doc.metadata['page_number']),
            'source': doc.metadata['source']
        }

    # create embeddings
    index_name = os.getenv('PINECONE_INDEX_NAME')
    embeddings = OpenAIEmbeddings()
    index = pinecone.Index(index_name)
    index.delete(delete_all=True)
    # ingest the rules document into the Vector DB
    Pinecone.from_documents(docs, embedding=embeddings, index_name=index_name)
    return docs


def get_relevant_docs(question: str) -> list[Document]:
    """Get the most relevant documents for a given question"""
    index_name = os.getenv('PINECONE_INDEX_NAME')
    index = pinecone.Index(index_name)
    embeddings = OpenAIEmbeddings()
    vector_db = Pinecone(index, embeddings.embed_query, 'text')
    return vector_db.similarity_search(question, k=2)
