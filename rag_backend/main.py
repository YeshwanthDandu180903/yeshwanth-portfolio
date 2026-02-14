from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later replace with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    message: str

# Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are Yeshwanth Dandu’s AI Portfolio Assistant.
Answer professionally about his skills, projects and experience.
Do not hallucinate.
Keep answers clear and concise.
"""

@app.get("/")
def home():
    return {"status": "Backend Running Successfully"}

@app.post("/chat")
async def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.message}
        ]
    )

    return {"response": response.choices[0].message.content}
