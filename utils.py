import subprocess
import whisper
import torch
import os
from dotenv import load_dotenv
from streamlit import cache_resource
from langchain_google_genai import ChatGoogleGenerativeAI

# Load .env
load_dotenv()

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
USE_FP16 = torch.cuda.is_available()

@cache_resource(show_spinner="Loading Whisper model…")
def load_whisper_model(model_name: str):
    model = whisper.load_model(model_name)
    return model.to(DEVICE)

@cache_resource(show_spinner="Initializing Gemini LLM…")
def load_gemini_llm(model_name: str, temperature: float = 0.2):
    api_key = os.getenv("GEMINI_API_KEY")
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key
    )

def ffmpeg_to_wav(src: str) -> str:
    dst = src + ".wav"
    subprocess.run(
        ["ffmpeg", "-y", "-i", src, "-ar", "16000", "-ac", "1", dst],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return dst
