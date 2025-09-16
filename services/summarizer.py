import os
from utils.chunker import chunk_text
from dotenv import load_dotenv
import google.generativeai as genai  # ✅ correct import

# Load environment variables
load_dotenv()

# Configure Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_text(text: str) -> str:
    chunks = chunk_text(text, max_chars=10000)
    summaries = []

    for chunk in chunks:
        response = genai.GenerativeModel("gemini-2.5-flash").generate_content(
            f"Generate a concise summary of the following text:\n{chunk}"
        )
        summaries.append(response.text)

    if len(summaries) == 1:
        return summaries[0]
    else:
        combined = " ".join(summaries)
        response = genai.GenerativeModel("gemini-2.5-flash").generate_content(
            f"Generate a concise summary of the following summaries:\n{combined}"
        )
        return response.text
