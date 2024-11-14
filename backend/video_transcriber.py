from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import whisper
import os
from fastapi import HTTPException


async def get_video_transcript(url: str, language: str = "mr") -> str:
    try:
        # YouTube first
        video_id = url.split("watch?v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return " ".join([entry['text'] for entry in transcript])
    except Exception as yt_error:
        try:
            # Fallback to Whisper
            model = whisper.load_model("base")
            yt = YouTube(url)
            audio_path = yt.streams.filter(only_audio=True).first().download()
            result = model.transcribe(audio_path)
            os.remove(audio_path)  # Cleaning up a downloaded file (Metro Boomin lol)
            return result["text"]
        except Exception as whisper_error:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get transcript: {str(whisper_error)}"
            )
