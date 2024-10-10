import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
logger = logging.getLogger(__name__)

def to_dict(obj):
    if hasattr(obj, "__dict__"):
        # convert object with a __dict__ to a dictionary
        result = {key: to_dict(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, list):
        # apply to_dict to each item in list
        result = [to_dict(item) for item in obj]
    else:
        # if it's not a custom object or list, just return it as is
        result = obj
    return result

def extract_transcript(audio_file: Path, subfolder: Path) -> Path:
    logger.info(f"Transcribing audio from {audio_file.stem}...")

    original_stem = audio_file.stem.rsplit('.', 1)[0]  # Remove '.compressed_audio' from the stem
    transcript_json_path = subfolder / f"{original_stem}.transcript.json"
    transcript_txt_path = subfolder / f"{original_stem}.transcript.txt"

    if transcript_json_path.exists() and transcript_txt_path.exists():
        logger.info(f"Transcript files already exist. Skipping transcription.")
        return transcript_json_path

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        with open(str(audio_file), 'rb') as audio_data:
            result = client.audio.transcriptions.create(model="whisper-1", file=audio_data,
                                                        response_format="verbose_json")
        transcript = to_dict(result)

        with open(transcript_json_path, 'w') as json_file:
            json.dump(transcript, json_file, indent=4)

        with open(transcript_txt_path, 'w') as txt_file:
            txt_file.write(transcript["text"])

        logger.info(f"Transcription saved to {transcript_json_path} and {transcript_txt_path}")
        return transcript_json_path
    except Exception as e:
        logging.error(f"Failed to transcribe audio file {audio_file}: {e}")
        # Clean up any partially written files
        for path in [transcript_json_path, transcript_txt_path]:
            if path.exists():
                path.unlink()
        raise
