from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware

openai.api_key = "your_openai_api_key"

app = FastAPI()

# CORS to allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

class EssayInput(BaseModel):
    essay: str

@app.post("/check-essay")
def check_essay(data: EssayInput):
    prompt = f"""
    You are a certified IELTS examiner. Analyze the following essay:
    
    {data.essay}
    
    Provide:
    1. An estimated IELTS band score (Task Response, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy).
    2. List of mistakes with explanations.
    3. Suggestions for improvement.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [{"role": "user", "content": prompt}]
    )
    return {"result": response.choices[0].message.content}
