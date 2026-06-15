from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import json

app = FastAPI()

# CORS settings - Streamlit frontend ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein specific URL daalna
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "AI Video Assistant Backend is Running!", "status": "active"}

@app.post("/process-video")
async def process_video(request: VideoRequest):
    try:
        print(f"Processing video: {request.url}")
        
        # YouTube video info extract karein bina download kiye
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Sirf info chahiye, download nahi
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(request.url, download=False)
                
                result = {
                    "success": True,
                    "title": info.get('title', 'No title'),
                    "duration": info.get('duration', 0),
                    "channel": info.get('uploader', 'Unknown'),
                    "views": info.get('view_count', 0),
                    "message": "Video info fetched successfully"
                }
                
                return result
                
            except Exception as e:
                print(f"YT-DLP Error: {str(e)}")
                raise HTTPException(
                    status_code=403, 
                    detail=f"Cannot fetch video: {str(e)}"
                )
                
    except Exception as e:
        print(f"General Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}