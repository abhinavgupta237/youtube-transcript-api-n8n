from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Optional: Enable CORS if calling from browser or other origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    try:
        # Get transcript options list for the video
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Prefer manually created English transcript, fallback to auto-generated
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except NoTranscriptFound:
            transcript = transcript_list.find_generated_transcript(['en'])

        data = transcript.fetch()

        # Filter empty lines or music markers and extract text
        lines = [entry['text'].strip() for entry in data if entry.get('text') and entry['text'].strip() != '[Music]']
        
        return {"text": lines}

    except TranscriptsDisabled:
        return {"error": "Transcripts are disabled for this video"}
    
    except Exception as e:
        return {"error": str(e)}
