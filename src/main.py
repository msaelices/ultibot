import sys
from io import BytesIO

import requests
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

from dotenv import load_dotenv
from PyPDF2 import PdfReader


def main() -> int:
    load_dotenv()
    st.set_page_config(page_title='Ultibot', page_icon=':frisbee:')
    st.header('Ultibot, tu experto en Ultimate Frisbee 💬')

    # RULES_URL = 'https://usaultimate.org/wp-content/uploads/2022/01/Official-Rules-of-Ultimate-2022-2023.pdf'
    RULES_URL = 'https://topultimatepa.files.wordpress.com/2021/06/wfdf-rules-of-ultimate-2021-2024-esp-universal-1.pdf'
    response = requests.get(RULES_URL)
    if not response.ok:
        st.exception(RuntimeError('Error fetching Ultimate Frisbee rules'))
        return 1
    reader = PdfReader(BytesIO(response.content))
    rules_text = ""
    for page in reader.pages:
        rules_text += page.extract_text()

    # split rules into chunks
    text_splitter = CharacterTextSplitter(
      separator='\n',
      chunk_size=2000,
      chunk_overlap=200,
      length_function=len
    )
    chunks = text_splitter.split_text(rules_text)

    # create embeddings
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_texts(chunks, embeddings)
    question = st.text_area('Haz una pregunta sobre las reglas de Ultimate 🥏:')
    if question:
        relevant_docs = vector_db.similarity_search(question, k=3)

        llm = OpenAI(model_name='text-davinci-003')
        qa_chain = load_qa_chain(llm, verbose=False)

        with get_openai_callback() as cb:
            response = qa_chain.run(input_documents=relevant_docs, question=question)
            # print tokens count and cost information
            print(cb)
            st.write(response)
    return 0

if __name__ == '__main__':
    sys.exit(main())