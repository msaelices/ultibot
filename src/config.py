from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    pinecone_api_key: str
    pinecone_region: str

    class Config:
        env_file = '.env'