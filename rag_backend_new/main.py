from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import sys

# Add current directory to path just in case
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our RAG agent
try:
    import rag_agent
    print(f"DEBUG PRE-IMPORT: Loading rag_agent from: {rag_agent.__file__}")
    from rag_agent import PortfolioAgent
except ImportError:
    print("Warning: Could not import rag_agent. Ensure rag_agent.py is in the same directory.")
    PortfolioAgent = None

load_dotenv()

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Initialize Agent
agent = None
try:
    if PortfolioAgent:
        print("Initializing Portfolio Agent...")
        agent = PortfolioAgent()
        print("Portfolio Agent initialized successfully.")
    else:
        print("PortfolioAgent class not available.")
except Exception as e:
    print(f"Error initializing agent: {e}")

@app.get("/")
def home():
    status = "RAG Backend Running"
    if agent:
        status += " with Agent Active"
    else:
        status += " (Agent Failed to Load)"
    return {"status": status}

@app.post("/chat")
async def chat(request: ChatRequest):
    if not agent:
        return {"response": "Error: RAG Agent is not active. Please check backend logs."}
    
    try:
        response = agent.get_response(request.message)
        return {"response": response}
    except Exception as e:
        print(f"Error during chat: {e}")
        return {"response": f"I'm encountering an error: {str(e)}"}

@app.get("/linkedin_posts")
async def linkedin_posts():
    if not agent:
        return {"error": "Error: RAG Agent is not active."}
    
    try:
        response = agent.generate_linkedin_content()
        return {"content": response}
    except Exception as e:
        print(f"Error generating LinkedIn content: {e}")
        return {"error": f"Error: {str(e)}"}
