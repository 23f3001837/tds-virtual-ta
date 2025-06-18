from dotenv import load_dotenv
import os
from pinecone import Pinecone

load_dotenv()  # Loads variables from .env

api_key = os.getenv('PINECONE_API_KEY')
if not api_key:
    raise ValueError('PINECONE_API_KEY not found in environment variables!')

# Initialize Pinecone and your assistant
pc = Pinecone(api_key=api_key)
assistant = pc.assistant.Assistant(assistant_name="tds-virtual-assistant")

# List of your JSON files
files_to_upload = [
    "data/discourse.json",
    "data/tds_website.json"
]

for file_path in files_to_upload:
    response = assistant.upload_file(file_path)
    print(f"Uploaded {file_path}: {response}")
