import os
from dotenv import load_dotenv
load_dotenv()
CHROMA_PATH=os.getenv("CHROMA_PATH","./chroma_db")
COLLECTION_NAME=os.getenv("COLLECTION_NAME","product_manuals")
GEMINI_MODEL=os.getenv("GEMINI_MODEL","gemini-2.0-flash")
