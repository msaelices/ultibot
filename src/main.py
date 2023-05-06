import sys

import langchain  # noqa: F401
import requests
import streamlit as st

from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS


def get_rules_prompt() -> PromptTemplate:
    template = """Given the following extracted parts of a long document with the Ultimate Frisbee rules and a question, create a final answer with references ("FUENTES"). 
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "FUENTES" part in your answer.
Respond in Spanish.

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER IN SPANISH:"""
    return PromptTemplate(template=template, input_variables=['summaries', 'question'])


def main() -> int:
    load_dotenv()
    st.set_page_config(page_title='Ultibot', page_icon=':frisbee:')
    st.header('Ultibot, tu experto en Ultimate Frisbee 💬')

    # RULES_URL = 'https://usaultimate.org/wp-content/uploads/2022/01/Official-Rules-of-Ultimate-2022-2023.pdf'
    RULES_URL = 'https://topultimatepa.files.wordpress.com/2021/06/wfdf-rules-of-ultimate-2021-2024-esp-universal-1.pdf'

    loader = PyMuPDFLoader(RULES_URL)
    docs = loader.load()

    # create embeddings
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_documents(docs, embedding=embeddings)
    question = st.text_area('Haz una pregunta sobre las reglas de Ultimate 🥏:')
    if question:
        relevant_docs = vector_db.similarity_search(question, k=1)

        llm = OpenAI(model_name='text-davinci-003')
        llm.set_verbose(False)

        qa_chain = load_qa_with_sources_chain(llm, verbose=False, prompt=get_rules_prompt())

        with get_openai_callback() as cb:
            response = qa_chain.run(input_documents=relevant_docs, question=question)
            # print tokens count and cost information
            print(cb)
            st.write(response)
    return 0

if __name__ == '__main__':
    sys.exit(main())