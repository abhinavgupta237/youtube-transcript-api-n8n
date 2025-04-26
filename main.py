@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # First try manually created English
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except NoTranscriptFound:
            try:
                # Then try auto-generated English
                transcript = transcript_list.find_generated_transcript(['en'])
            except NoTranscriptFound:
                # Final fallback: try Hindi (auto-generated)
                transcript = transcript_list.find_transcript(['hi'])

        data = transcript.fetch()

        # Clean the output
        lines = [entry['text'].strip() for entry in data if entry.get('text') and entry['text'].strip() != '[Music]']
        return {"text": lines}

    except TranscriptsDisabled:
        return {"error": "Transcripts are disabled for this video"}

    except Exception as e:
        return {"error": str(e)}
