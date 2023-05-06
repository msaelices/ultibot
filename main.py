import os
import sys

import langchain  # noqa: F401
import streamlit as st

from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file before importing any other modules

from langchain.callbacks import get_openai_callback
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from brain import get_relevant_docs


def get_rules_prompt(lang: str) -> PromptTemplate:
    language = 'Spanish' if lang == 'es' else 'English'
    reference = 'FUENTES' if lang == 'es' else 'SOURCES'
    template = f"""Given the following extracted parts of a long document with the Ultimate Frisbee rules and a question, create a final answer with references ("{reference}"). 
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "{reference}" part in your answer.
Respond in {language}.

QUESTION: {{question}}
=========
{{summaries}}
=========
FINAL ANSWER IN {language}:"""
    return PromptTemplate(template=template, input_variables=['summaries', 'question'])


headers = {
    'es': 'Ultibot, tu experto en Ultimate Frisbee',
    'en': 'Ultibot, your Ultimate Frisbee expert'
}

input_labels = {
    'es': 'Haz una pregunta sobre las reglas de Ultimate',
    'en': 'Ask a question about the Ultimate rules'
}

languages = {
    'es': 'Spanish',
    'en': 'English',
}


def main() -> int:
    lang = os.getenv('UI_LANGUAGE', 'en')
    st.set_page_config(page_title='Ultibot', page_icon=':frisbee:')
    st.header(f'{headers[lang]} 💬')

    # create embeddings
    question = st.text_area(f'{input_labels[lang]} 🥏:')
    if question:
        relevant_docs = get_relevant_docs(question)

        llm = OpenAI(model_name='text-davinci-003')
        llm.set_verbose(False)

        qa_chain = load_qa_with_sources_chain(llm, verbose=False, prompt=get_rules_prompt(lang))

        with get_openai_callback() as cb:
            response = qa_chain.run(input_documents=relevant_docs, question=question)
            # print tokens count and cost information
            print(cb)
            st.write(response)
    return 0

if __name__ == '__main__':
    sys.exit(main())