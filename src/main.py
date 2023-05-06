import sys
from io import BytesIO

import requests
import streamlit as st

from dotenv import load_dotenv
from PyPDF2 import PdfReader


def main() -> int:
    load_dotenv()
    st.set_page_config(page_title='Ask your Ultimate Frisbee Chatbot expert')
    st.header("Ask Ultimate Frisbee Chatbot expert 💬")

    RULES_URL = 'https://usaultimate.org/wp-content/uploads/2022/01/Official-Rules-of-Ultimate-2022-2023.pdf'
    response = requests.get(RULES_URL)
    if not response.ok:
        st.exception(RuntimeError('Error fetching Ultimate Frisbee rules'))
        return -1
    reader = PdfReader(BytesIO(response.content))


if __name__ == '__main__':
    sys.exit(main())