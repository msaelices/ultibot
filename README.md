# Ultibot

Ultimate Frisbee Chatbot, made with FastAPI and Vue.js

## Set-up

### Backend setup

Create a new virtual environment and activate it:

    python -m venv env/
    source env/bin/activate

Install the needed dependencies:

    pip install -r requirements.txt

Copy the `.env-default` file to `.env` file and fill it with your API keys:

    cd src/
    cp .env-default .env

### Starting the server

For starting the FastAPI Server, go to the `src` directory and run `uvicorn` with the following command:

    uvicorn --reload main:app --host 0.0.0.0 --port 8080

Or just:

    python main.py

Then, navigate to the http://localhost:8080/chat/