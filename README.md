# 📂🌳 filetree-leafbloomer 🍃🌸

Crawl your filetree and apply a custom processing pipeline to its artifacts in the leaves, things like-- audio extraction, transcription, summarization, and html generation.

> AI gen below.

## Quick Explanation

📂🌳 filetree-leafbloomer 🍃🌸 is a tool that processes video files to extract audio, compress it, generate transcripts, create summaries, and generate word clouds. It also creates HTML summaries for easy viewing. Perfect for turning your videos into digestible content!

## Install Instructions

1. **Clone the repository:**

    ```sh
    git clone https://github.com/JacKaL37/filetree-leafbloomer.git
    cd filetree-leafbloomer
    ```

2. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    Create a `.env` file in the root directory and add your `OPENAI_API_KEY`:

    ```sh
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Usage

Run the tool using the following command:

```sh
python main.py <directory> [--exclude <files_or_folders_to_exclude>]
```

### Parameters

- `directory` (required): The directory containing video files to process.
- `--exclude` (optional): List of files or folders to exclude from processing.

### Example

To process all videos in the `testing_data/` directory and exclude the `intro` videos:

```sh
python main.py .\testing_data --exclude intro.mp4
```

### Output

- **Audio Extraction:** Extracts audio from video and saves it in the same folder.
- **Audio Compression:** Compresses the extracted audio.
- **Transcript Extraction:** Generates a transcript from the compressed audio.
- **Summarization:** Summarizes the transcript.
- **Word Cloud Generation:** Generates a word cloud from the transcript.
- **HTML Summary:** Creates an HTML summary for easy viewing.

## Additional Scripts

- **Renamer Script:**

    Renames files according to a specific pattern (first version to next):

    ```sh
    python util/renamer_v1-v2.py <directory>
    ```

- **Collect Source Code:**

    Quine-adjacent, collects the source code and file structure into a markdown file AND the clipboard directly!

    ```sh
    python util/collect_source_code.py
    ```

---

🚀 Get ready to transform your video content into rich, summarized insights with 🌳 filetree-leafbloomer 🌸!
