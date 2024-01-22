import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain.agents import tool
from supabase.client import Client, create_client
from dotenv import load_dotenv


load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = OpenAIEmbeddings()

vector_store = SupabaseVectorStore(
    embedding=embeddings,
    client=supabase,
    table_name="xyventures",
    query_name="match_xyventures",
)


@tool
def get_current_info_from_xyventures(query: str) -> str:
    """Returns the computed mortgage rate based on the input values for loan amount, interest rate and terms."""

    retriever = vector_store.as_retriever()

    results = retriever.get_relevant_documents(query)

    reply = results[0].page_content

    data = {"output": reply}

    return data
