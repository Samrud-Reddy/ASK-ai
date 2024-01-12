import os
from dotenv import load_dotenv
import google.generativeai as genai
import pinecone

load_dotenv()

GEMINI_API_KEY = str(os.getenv("GEMINI_API_KEY"))
PINECONE_API_KEY = str(os.getenv("VECTOR_API_KEY"))

genai.configure(api_key=GEMINI_API_KEY)

def get_embedings(text: str, title: str):
    return genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document",
        title=title,
    )["embedding"]


print(get_embedings("Hehihi", "sd"))

pinecone.init(api_key=PINECONE_API_KEY, environment="gcp-starter")
index = pinecone.Index("textbooks")

index.upsert([
    ("A", get_embedings("Hello dodo", "chem")),
])


