# main.py - FastAPI Backend for AI Video Assistant
# Root folder wala - Ye core/ aur utils/ folders ke saath kaam karega

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import logging
import time
from datetime import datetime
import yt_dlp
import os

# ============ YOUR EXISTING MODULES ============
# Ye aapke core/ aur utils/ folders se import karta hai
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

# Load environment variables
load_dotenv()

# ============ LOGGING SETUP ============
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============ FASTAPI APP ============
app = FastAPI(
    title="AI Video Assistant API",
    description="Turn YouTube videos into actionable insights",
    version="1.0.0"
)

# ============ CORS SETUP (for Streamlit frontend) ============
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein specific URL daalna
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ REQUEST/RESPONSE MODELS ============
class VideoRequest(BaseModel):
    url: str
    language: Optional[str] = "english"

class ChatRequest(BaseModel):
    question: str
    session_id: str

# ============ STORE RAG CHAINS IN MEMORY ============
rag_chains: Dict[str, Any] = {}

# ============ YOUR ORIGINAL run_pipeline FUNCTION ============
def run_pipeline(source: str, language: str = "english") -> dict:
    """
    Your original pipeline - exactly as you had it in CLI version
    """
    print("starting AI Video Assistant")
    
    chunks = process_input(source)
    transcript = transcribe_all(chunks, language)
    print(f"raw transcription (first 300 characters) {transcript[:300]}")
    
    title = generate_title(transcript)
    summary = summarize(transcript)
    action_item = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)
    rag_chain = build_rag_chain(transcript)
    
    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_item,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }

# ============ HELPER: GET VIDEO DURATION ============
def get_video_duration(url: str) -> int:
    """Get video duration in seconds to prevent timeout"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('duration', 0)
    except Exception as e:
        logger.error(f"Failed to get duration: {e}")
        return 0

# ============ API ENDPOINTS ============

@app.get("/")
def home():
    return {
        "message": "AI Video Assistant Backend is Running!",
        "status": "active",
        "endpoints": ["/", "/health", "/process-video", "/chat"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/process-video")
async def process_video(request: VideoRequest):
    """
    Process YouTube video or local file
    Returns: title, transcript, summary, action items, decisions, questions
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing video: {request.url}")
        
        # Optional: Check video duration (prevents timeout on very long videos)
        duration = get_video_duration(request.url)
        if duration > 600:  # 10 minutes max
            logger.warning(f"Video too long: {duration//60} minutes")
            # Still process, but log warning
        
        # Run your original pipeline
        result = run_pipeline(request.url, request.language)
        
        # Create session ID for chat
        session_id = f"session_{int(time.time())}"
        rag_chains[session_id] = result["rag_chain"]
        
        processing_time = time.time() - start_time
        logger.info(f"Pipeline completed in {processing_time:.2f} seconds")
        
        # Return response (transcript truncated for performance)
        return {
            "success": True,
            "title": result["title"],
            "transcript": result["transcript"][:3000] + "..." if len(result["transcript"]) > 3000 else result["transcript"],
            "summary": result["summary"],
            "action_items": result["action_items"],
            "key_decisions": result["key_decisions"],
            "open_questions": result["open_questions"],
            "session_id": session_id,
            "processing_time": round(processing_time, 2)
        }
        
    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.post("/chat")
async def chat_with_video(request: ChatRequest):
    """
    Ask questions about the processed video using RAG
    """
    try:
        if request.session_id not in rag_chains:
            raise HTTPException(
                status_code=404,
                detail="Session not found. Please process a video first."
            )
        
        rag_chain = rag_chains[request.session_id]
        answer = ask_question(rag_chain, request.question)
        
        return {
            "answer": answer,
            "session_id": request.session_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.delete("/session/{session_id}")
def clear_session(session_id: str):
    """Clear RAG chain from memory"""
    if session_id in rag_chains:
        del rag_chains[session_id]
        return {"message": f"Session {session_id} cleared"}
    return {"message": "Session not found"}

# ============ CLI MODE (Your Original Command Line Interface) ============
if __name__ == "__main__":
    import uvicorn
    import sys
    
    # Check if CLI mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        # Your original CLI code
        print("=" * 60)
        print("🎬 AI Video Assistant - CLI Mode")
        print("=" * 60)
        source = input("Enter YouTube URL or local file path: ").strip()
        language = input("Language (english/hinglish): ").strip() or "english"
        
        result = run_pipeline(source, language)
        
        print("\n" + "=" * 60)
        print(f"📌 Title: {result['title']}")
        print(f"\n📋 Summary:\n{result['summary']}")
        print(f"\n✅ Action Items:\n{result['action_items']}")
        print(f"\n🔑 Key Decisions:\n{result['key_decisions']}")
        print(f"\n❓ Open Questions:\n{result['open_questions']}")
        print("=" * 60)
        
        # Phase 2 — Chat with your meeting via RAG
        print("\n💬 Chat with your meeting (type 'exit' to quit)\n")
        rag_chain = result["rag_chain"]
        while True:
            question = input("You: ").strip()
            if question.lower() in ["exit", "quit", "q"]:
                print("👋 Goodbye!")
                break
            if not question:
                continue
            answer = ask_question(rag_chain, question)
            print(f"\n🤖 Assistant: {answer}\n")
    
    else:
        # FastAPI server mode (default)
        print("=" * 60)
        print("🚀 AI Video Assistant - FastAPI Server Mode")
        print("=" * 60)
        print(f"📍 Server running at: http://localhost:8000")
        print(f"📚 API Documentation: http://localhost:8000/docs")
        print(f"💚 Health Check: http://localhost:8000/health")
        print("=" * 60)
        print("\nPress CTRL+C to stop the server\n")
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=True
        )