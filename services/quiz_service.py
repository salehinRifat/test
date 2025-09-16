import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_quiz(text: str, num_questions: int = 5):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        Create {num_questions} multiple-choice quiz questions 
        based on the following text:

        {text}

        Format the response strictly as JSON without any markdown formatting:
        {{
          "quiz": [
            {{
              "question": "string",
              "options": ["A", "B", "C", "D"],
              "answer": "Correct option"
            }}
          ]
        }}
        """

        response = model.generate_content(prompt)
        
        # Clean up the response text to extract JSON
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```'):
            response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
            response_text = re.sub(r'\n?```$', '', response_text)
        
        # Try to parse as JSON
        try:
            quiz_data = json.loads(response_text)
            return quiz_data
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured error
            return {
                "error": "Failed to parse quiz response",
                "raw_response": response_text[:500]  # First 500 chars for debugging
            }
            
    except Exception as e:
        return {
            "error": f"Failed to generate quiz: {str(e)}"
        }
