import logging
from pathlib import Path
from pydub import AudioSegment

logger = logging.getLogger(__name__)

def compress_audio(audio_file: Path, subfolder: Path) -> Path:
    logger.info(f"Compressing audio file {audio_file.stem}...")
    
    original_stem = audio_file.stem.rsplit('.', 1)[0]  # Remove '.audio' from the stem
    compressed_audio_file = subfolder / f"{original_stem}.compressed_audio.mp3"
    incomplete_path = subfolder / f"{original_stem}.compressed_audio.mp3.incomplete"
    
    if compressed_audio_file.exists():
        logger.info(f"Compressed audio file {compressed_audio_file} already exists. Skipping compression.")
        return compressed_audio_file
    
    try:
        audio = AudioSegment.from_file(audio_file)
        audio.export(incomplete_path, format="mp3", bitrate="32k")
        incomplete_path.rename(compressed_audio_file)
        logger.info(f"Compressed audio file {audio_file.stem} to {compressed_audio_file}.")
        return compressed_audio_file
    except Exception as e:
        logger.error(f"Failed to compress audio file {audio_file}: {e}")
        if incomplete_path.exists():
            incomplete_path.unlink()
        raise
