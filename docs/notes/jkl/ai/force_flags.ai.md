To enable "force" flags for specific process steps, you'll need to modify your `main.py` file and the individual process functions. Here's how you can implement this feature:

1. First, update the `main.py` file to accept force flags as command-line arguments:

```python
import argparse

# ... (existing imports)

def main(directory: str, exclude: List[str], force: List[str]):
    path = Path(directory)
    
    for video_file in path.rglob('*.mp4'):
        if not is_excluded(video_file, exclude):
            process_video_file(video_file, exclude, force)

def process_video_file(video_file: Path, exclude: List[str], force: List[str]):
    subfolder = video_file.parent / video_file.stem
    subfolder.mkdir(exist_ok=True)

    try:
        audio_file = extract_audio(video_file, subfolder, 'extract_audio' in force)
        compressed_audio = compress_audio(audio_file, subfolder, 'compress_audio' in force)
        transcript_file = extract_transcript(compressed_audio, subfolder, 'extract_transcript' in force)
        summary_file = summarize_transcript(transcript_file, subfolder, 'summarize_transcript' in force)  
        html_summary_file = generate_html_summary(summary_file, subfolder, 'generate_html_summary' in force)
    except Exception as e:
        logging.error(f"Failed to process {video_file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video files to extract audio and transcripts.")
    parser.add_argument("directory", help="Directory containing video files to process")
    parser.add_argument("--exclude", nargs="*", default=[], help="Files or folders to exclude")
    parser.add_argument("--force", nargs="*", default=[], choices=['extract_audio', 'compress_audio', 'extract_transcript', 'summarize_transcript', 'generate_html_summary'], 
                        help="Force specific processes to run even if output already exists")
    
    args = parser.parse_args()
    main(args.directory, args.exclude, args.force)
```

2. Next, update each process function to accept a `force` parameter. Here's an example using the `extract_audio` function:

```python
def extract_audio(video_file: Path, subfolder: Path, force: bool = False) -> Path:
    logging.info(f"Extracting audio from {video_file.stem}...")
    
    audio_output_path = subfolder / f"{video_file.stem}.audio.mp3"
    incomplete_path = subfolder / f"{video_file.stem}.audio.mp3.incomplete"
    
    if audio_output_path.exists() and not force:
        logging.info(f"Audio file {audio_output_path} already exists. Skipping extraction.")
        return audio_output_path
    
    try:
        extract_audio_core(input_path=str(video_file), output_path=str(incomplete_path), overwrite=True)
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
```

3. Apply similar changes to the other process functions (`compress_audio`, `extract_transcript`, `summarize_transcript`, and `generate_html_summary`).

With these changes, you can now use the `--force` flag when running the script to force specific processes to run, even if their output already exists. For example:

```
python main.py /path/to/videos --force extract_audio summarize_transcript
```

This will force the audio extraction and transcript summarization steps to run, even if their outputs already exist, while other steps will still skip if their outputs are present.
