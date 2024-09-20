import logging
from pathlib import Path
from audio_extract import extract_audio as extract_audio_core

def extract_audio(video_file: Path, subfolder: Path) -> Path:
    logging.info(f"Extracting audio from {video_file.stem}...")
    
    audio_output_path = subfolder / f"{video_file.stem}.audio.mp3"
    incomplete_path = subfolder / f"{video_file.stem}.audio.mp3.incomplete"
    
    if audio_output_path.exists():
        logging.info(f"Audio file {audio_output_path} already exists. Skipping extraction.")
        return audio_output_path
    
    try:
        extract_audio_core(input_path=str(video_file), output_path=str(incomplete_path), overwrite=True)
        # The actual output file will have .mp3 appended, so we need to account for that
        actual_incomplete_path = incomplete_path.with_suffix('.incomplete.mp3')
        actual_incomplete_path.rename(audio_output_path)
        logging.info(f"Extracted audio from {video_file.stem} to {audio_output_path}.")
        return audio_output_path
    except Exception as e:
        logging.error(f"Failed to extract audio from {video_file}: {e}")
        actual_incomplete_path = incomplete_path.with_suffix('.incomplete.mp3')
        if actual_incomplete_path.exists():
            actual_incomplete_path.unlink()
        raise
