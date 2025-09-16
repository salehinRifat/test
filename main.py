from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services import summarizer, pdf_service, quiz_service

app = FastAPI(title="AI Summarizer API")

class QuizRequest(BaseModel):
    text: str
    num_questions: int = 5

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize-text")
async def summarize_text(text: str = Form(...)):
    return {"summary": summarizer.summarize_text(text)}

@app.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile):
    text = pdf_service.extract_text(file)
    return {"summary": summarizer.summarize_text(text)}

@app.post("/generate-quiz")
def create_quiz(request: QuizRequest):
    quiz = quiz_service.generate_quiz(request.text, request.num_questions)
    return {"quiz": quiz}

@app.get("/")
async def root():
    return {"message": "AI Summarizer API is running!"}

# ✅ Only needed for local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
