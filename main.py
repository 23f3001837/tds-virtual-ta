from fastapi import FastAPI, HTTPException
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
import json

from pydantic import BaseModel
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from typing import Optional
from dotenv import load_dotenv
import uvicorn
import os


load_dotenv() 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('pinecone_api_key'))
assistant = pc.assistant.Assistant(assistant_name="tds-virtual-assistant")

# Request model
class QueryRequest(BaseModel):
    question: str
    image: Optional[str] = None

# Response model (matches expected format)
class QueryResponse(BaseModel):
    answer: str
    links: list[dict[str, str]]

@app.post("/api/", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        # Debug: Print environment and request
        #print("Pinecone API key:", os.getenv('PINECONE_API_KEY'))
        print("Assistant name:", assistant.assistant_name)
        print("Received question:", request.question)
        if request.image:
            print("Received image (truncated):", str(request.image)[:100])

        # Prepare message for Pinecone assistant
        message = {
            "role": "user",
            "content": request.question
        }
        if request.image:
            message["image"] = {"data": request.image}

        # Get response from Pinecone assistant
        resp = assistant.chat(messages=[message])
        print("Raw Pinecone response:", resp)
        response_data = resp["message"].get("content", None)
        print("Raw content:", response_data)

        # If response is a string, try to parse it as JSON (in case Pinecone returns JSON as string)
        import json
        if isinstance(response_data, str):
            try:
                response_data = json.loads(response_data)
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Pinecone response was not valid JSON: " + str(response_data))
        if not response_data or not isinstance(response_data, dict):
            raise HTTPException(status_code=500, detail="Pinecone response missing or not a dict: " + str(response_data))
        if "answer" not in response_data or "links" not in response_data:
            raise HTTPException(status_code=500, detail="Pinecone response missing 'answer' or 'links': " + str(response_data))
        return QueryResponse(**response_data)
    except Exception as e:
        print("Exception in process_query:", str(e))
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/api/test")
async def test(): 
    return {"response": "Test Done"}

@app.get("/")
async def home(): 
    return {"response": "Who are u?"}
