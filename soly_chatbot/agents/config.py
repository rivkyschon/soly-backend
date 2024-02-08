import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
model = ChatOpenAI(model="gpt-4-1106-preview", openai_api_key=os.getenv('OPENAI_API_KEY'))
