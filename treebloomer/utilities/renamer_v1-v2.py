import os
from pathlib import Path

def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = Path(root) / file
            parent_dir = path.parent
            source_stem = parent_dir.name

            # Skip the source video file
            if file.endswith('.mp4'):
                continue

            new_name = None

            if file == f"{source_stem}_audio.mp3":
                new_name = f"{source_stem}.audio.mp3"
            elif file == f"{source_stem}_audio_compressed.mp3":
                new_name = f"{source_stem}.compressed_audio.mp3"
            elif file == f"{source_stem}_whisper_transcript.json":
                new_name = f"{source_stem}.transcript.json"
            elif file == f"{source_stem}_whisper_transcript.txt":
                new_name = f"{source_stem}.transcript.txt"

            if new_name:
                new_path = parent_dir / new_name
                path.rename(new_path)
                print(f"Renamed: {path} -> {new_path}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python rename_script.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    rename_files(directory)
    print("File renaming complete.")
