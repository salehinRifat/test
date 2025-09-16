import os
from utils.chunker import chunk_text
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_text(text: str) -> str:
    # Break long text into chunks
    chunks = chunk_text(text, max_chars=10000)
    summaries = []

    for chunk in chunks:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Replace with your desired Gemini model
            contents=f"Generate a concise summary of the following text:\n{chunk}"
        )
        summaries.append(response.text)

    # If many chunks, summarize again
    if len(summaries) == 1:
        return summaries[0]
    else:
        combined = " ".join(summaries)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Generate a concise summary of the following summaries:\n{combined}"
        )
        return response.text
