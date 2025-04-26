from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to YouTube Transcript API!"}

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try manually created English transcript
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except NoTranscriptFound:
            try:
                # Try auto-generated English transcript
                transcript = transcript_list.find_generated_transcript(['en'])
            except NoTranscriptFound:
                # Final fallback: Hindi transcript (auto-generated)
                transcript = transcript_list.find_transcript(['hi'])

        data = transcript.fetch()

        # Remove empty text or just "[Music]" and strip whitespace
        lines = [entry['text'].strip() for entry in data if entry.get('text') and entry['text'].strip() != '[Music]']
        return {"text": lines}

    except TranscriptsDisabled:
        return {"error": "Transcripts are disabled for this video"}

    except NoTranscriptFound:
        return {"error": "Transcript not available in English or Hindi"}

    except Exception as e:
        return {"error": str(e)}
