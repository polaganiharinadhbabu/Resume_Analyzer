import base64
import os
import shutil
from pathlib import Path
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
import requests

app = FastAPI()


def get_gemini_api_key():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY is not configured.")
    return api_key

@app.get("/gemini/models")
def models():
     return {"models":["gemini-3.8-flash"]}

@app.post("/gemini/chat")
def chat(message:str):
    URL=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={get_gemini_api_key()}"
    payload={"contents":[{"role":"user","parts":[{"text":message}]}]}
    response=requests.post(URL,json=payload)
    response_data=response.json()
    text_output=response_data["candidates"][0]["content"]["parts"][0]["text"]
    return {"user_input":message,"response":text_output}


@app.post("/gemini/chat-with-file")
def chat_with_file(message: str = Form(...), file: UploadFile = File(...)):
    allowed_types = {"application/pdf", "image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail="Upload a PDF, JPEG, PNG, or WebP file.",
        )

    file_bytes = file.file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(file_bytes) > 20 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="The file must be 20 MB or smaller.")

    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={get_gemini_api_key()}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": file.content_type,
                            "data": base64.b64encode(file_bytes).decode("utf-8"),
                        }
                    },
                    {"text": message},
                ],
            }
        ]
    }

    response = requests.post(URL, json=payload, timeout=60)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    try:
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise HTTPException(
            status_code=502,
            detail="The AI service returned no answer for this file.",
        )

    return {"user_input": message, "filename": file.filename, "response": answer}


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Creates folder if it doesn't exist


@app.post("/gemini/resume")
def upload_file(file: UploadFile):
    destination = UPLOAD_DIR / file.filename

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"Saved {file.filename}p- fto {UPLOAD_DIR}"}


@app.post("/analyze-resume")
def analyze_resume(file: UploadFile):
    # 1. Read file bytes and convert to base64
    file_bytes = file.file.read()
    base64_data = base64.b64encode(file_bytes).decode("utf-8")

    # 2. Build the Gemini payload
    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={get_gemini_api_key()}"
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": file.content_type or "application/pdf",
                            "data": base64_data,
                        }
                    },
                    {
                        "text": "Analyze this resume. Give a quick summary, skills, strengths, and areas for improvement."
                    },
                ]
            }
        ]
    }


    response = requests.post(URL, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    result_text = data["candidates"][0]["content"]["parts"][0]["text"]

    return {"analysis": result_text}
