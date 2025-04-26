from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "YouTube Transcript API is working!"}

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try manually created English transcript
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except NoTranscriptFound:
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
            except NoTranscriptFound:
                transcript = transcript_list.find_transcript(['hi'])

        data = transcript.fetch()

        # Corrected: FetchedTranscriptSnippet is not a dict — use dot notation
        lines = [
            t.text.strip() for t in data
            if hasattr(t, "text") and t.text.strip() != "[Music]"
        ]

        return {"text": lines}

    except TranscriptsDisabled:
        return {"error": "Transcripts are disabled for this video"}
    except NoTranscriptFound:
        return {"error": "Transcript not available in English or Hindi"}
    except Exception as e:
        return {"error": str(e)}
