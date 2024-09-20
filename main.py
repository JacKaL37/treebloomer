import logging
from pathlib import Path
from typing import List
import argparse

from processes.audio_extraction import extract_audio
from processes.audio_compression import compress_audio
from processes.transcript_extraction import extract_transcript
from processes.summarization import summarize_transcript
from processes.html_page_generation import generate_html_summary
from processes.word_cloud_generation import generate_word_cloud


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_excluded(file_path: Path, exclude: List[str]) -> bool:
    return any(ex in file_path.parts for ex in exclude) or file_path.name in exclude

def process_video_file(video_file: Path, exclude: List[str]):
    subfolder = video_file.parent / video_file.stem
    subfolder.mkdir(exist_ok=True)

    try:
        audio_file = extract_audio(video_file, subfolder)
        compressed_audio = compress_audio(audio_file, subfolder)
        transcript_file = extract_transcript(compressed_audio, subfolder)
        summary_file = summarize_transcript(transcript_file, subfolder)  
        wordcloud_file = generate_word_cloud(transcript_file, subfolder)
        html_summary_file = generate_html_summary(summary_file, subfolder)
    except Exception as e:
        logging.error(f"Failed to process {video_file}: {e}")

def main(directory: str, exclude: List[str]):
    path = Path(directory)
    
    for video_file in path.rglob('*.mp4'):
        if not is_excluded(video_file, exclude):
            process_video_file(video_file, exclude)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video files to extract audio and transcripts.")
    parser.add_argument("directory", help="Directory containing video files to process")
    parser.add_argument("--exclude", nargs="*", default=[], help="Files or folders to exclude")
    
    args = parser.parse_args()
    main(args.directory, args.exclude)
