from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(model="gpt-4")
