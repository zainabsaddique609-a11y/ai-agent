from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import datetime
import os

app = FastAPI(title="AI Agent Assignment", description="Full-Stack AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    prompt: str

def run_ai_agent(prompt: str) -> str:
    query = prompt.lower()
    if "time" in query or "date" in query:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"⏰ [Tool Execution: Clock] Current system time and date: {current_time}"
    elif "summarize" in query:
        text_to_sum = prompt.replace("summarize", "").strip()
        if not text_to_sum:
            return "⚠️ Please provide text to summarize after the word 'summarize'."
        return f"📝 [Tool Execution: Text Summarizer]\nSummary: {text_to_sum[:100]}... (Processed successfully)."
    elif "code" in query or "python" in query:
        return "💻 [Tool Execution: Code Assistant]\nHere is a quick Python snippet:\n```python\ndef agent_loop(task):\n    print(f'Executing: {task}')\n    return 'Success'\n```"
    else:
        return f"🤖 [AI Agent Core Response]: I processed your request: '{prompt}'. Ready for your assignment!"

@app.get("/")
async def serve_frontend():
    html_path = "index.html"
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"error": "index.html file not found in the folder!"}

@app.post("/api/agent")
async def agent_endpoint(data: AgentRequest):
    if not data.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    response_text = run_ai_agent(data.prompt)
    return {"status": "success", "response": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)