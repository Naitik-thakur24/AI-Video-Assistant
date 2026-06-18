AI Video Assistant 🎥🤖
AI Video Assistant helps you save time by turning videos into actionable insights. Upload a video from local storage or paste a URL to instantly generate transcripts, AI-powered titles, concise summaries, and answers through a RAG engine. Perfect when you don't have time to watch the entire video.

✨ Features
📤 Upload Videos – Support for local video files

🔗 Paste URLs – Process videos directly from links

📝 Transcript Generation – Convert audio to accurate text

🤖 AI-Powered Titles – Automatically generate descriptive titles

📊 Concise Summaries – Get key points quickly

❓ RAG Engine – Ask questions and get answers about the video content

⚡ Fast & Efficient – Save time by not watching full videos

🛠️ Tech Stack
Backend: FastAPI (Python)

Frontend: (Streamlit)

Video Processing: yt-dlp, ffmpeg

AI/ML: RAG (Retrieval-Augmented Generation) engine

Language: Python 100%

📂 Project Structure
text
AI-Video-Assistant/
├── backend/          # FastAPI backend
├── core/             # Core functionality
├── utils/            # Utility functions
├── app.py            # Main application entry
├── main.py           # Application configuration
├── requirements.txt  # Python dependencies
├── packages.txt      # System packages (yt-dlp, ffmpeg)
└── test.py           # Test scripts
🚀 Getting Started
Prerequisites
Python 3.8+

FFmpeg

yt-dlp

Installation
Clone the repository

bash
git clone https://github.com/Naitik-thakur24/AI-Video-Assistant.git
cd AI-Video-Assistant
Install dependencies

bash
pip install -r requirements.txt
Install system packages (for yt-dlp & ffmpeg support)

bash
# On Ubuntu/Debian
sudo apt-get install ffmpeg
# Or use packages.txt for additional dependencies
Run the application

bash
python app.py
🔧 Configuration
The backend URL is configured to run on Render (production). For local development, update the backend URL in your frontend configuration:

python
# Change from render.com to localhost for development
BACKEND_URL = "http://localhost:8000"
🤝 Contributing
Contributions are welcome! Feel free to:

Report issues

Suggest new features

Submit pull requests

📊 Project Status
Stars: 0

Forks: 0

Watchers: 0

Latest Commit: June 15, 2026

Language: Python 100%

👨‍💻 Author
Naitik-thakur24

📄 License
This project is open source. Check the repository for license details.

