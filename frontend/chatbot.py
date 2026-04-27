import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# We expect GEMINI_API_KEY to be set in the environment or .env
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-001')
    except Exception as e:
        model = None
else:
    model = None

def get_chat_response(prompt: str, context: str) -> str:
    if not model:
        return "Gemini API key is missing or invalid. Please check your .env file."
    
    full_prompt = f"""
    You are an intelligent AI assistant for the Community Insight & Volunteer Matching System.
    Use the following current database context to answer the user's question.
    
    Context:
    {context}
    
    User Question: {prompt}
    
    Provide a helpful, concise, and professional answer.
    """
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"
