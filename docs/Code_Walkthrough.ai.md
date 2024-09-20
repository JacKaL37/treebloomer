# 🌳 filetree-leafbloomer 🌸 Code Execution Walkthrough

graph TD
    A[Video File (.mp4)] -->|Extract Audio| B[Audio File (.audio.mp3)]
    B -->|Compress Audio| C[Compressed Audio File (.compressed_audio.mp3)]
    C -->|Extract Transcript| D[Transcript Files (.transcript.json & .transcript.txt)]
    D -->|Summarize Transcript| E[Summary File (.summaries.json)]
    D -->|Generate Word Cloud| F[Word Cloud (.wordcloud.png)]
    E -->|Generate HTML Summary| G[HTML Summary (.html)]

    style A fill:#f9f,stroke:#333,stroke-width:4px
    style B fill:#ff9,stroke:#333,stroke-width:4px
    style C fill:#9ff,stroke:#333,stroke-width:4px
    style D fill:#9f9,stroke:#333,stroke-width:4px
    style E fill:#f99,stroke:#333,stroke-width:4px
    style F fill:#99f,stroke:#333,stroke-width:4px
    style G fill:#fa9,stroke:#333,stroke-width:4px


## Running the Main File

### Step-by-Step Guide

1. **Navigate to Project Directory:**
    ```sh
    cd path/to/filetree-leafbloomer
    ```

2. **Run the Main Script:**
    ```sh
    python main.py <directory> [--exclude <files_or_folders_to_exclude>]
    ```

### What Happens When You Run `main.py`?

1. **Parse Arguments:**
    - Directory to process
    - Optional exclusions

2. **Iterate Over Video Files:**
    - Looks for `.mp4` files in the specified directory

3. **For Each Video File:**
    - **Check Exclusions:**
        - Skip files/folders specified in `--exclude`
    - **Create Subfolder:**
        - Creates a subfolder with the same name as the video file without the extension

4. **Process Video File:**

    #### **Audio Extraction:**
    - **Input:** Video file
    - **What it does:** Extracts the audio track from the video
    - **Output:** `.audio.mp3` file
    - **Result:** Isolates the audio for further processing

    #### **Audio Compression:**
    - **Input:** Extracted audio file
    - **What it does:** Compresses the audio to reduce file size
    - **Output:** `.compressed_audio.mp3` file
    - **Result:** Smaller, more manageable audio file for transcription

    #### **Transcript Extraction:**
    - **Input:** Compressed audio file
    - **What it does:** Uses AI to transcribe the audio into text
    - **Output:** `.transcript.json` and `.transcript.txt` files
    - **Result:** Full text transcript of the audio

    #### **Summarization:**
    - **Input:** Transcript file
    - **What it does:** Analyzes and summarizes the transcript
    - **Output:** `.summaries.json` file
    - **Result:** Structured summaries and key points from the transcript

    #### **Word Cloud Generation:**
    - **Input:** Transcript file
    - **What it does:** Creates a visual word cloud from the transcript
    - **Output:** `.wordcloud.png` file
    - **Result:** Visual representation of frequently occurring words

    #### **HTML Summary:**
    - **Input:** Summary file
    - **What it does:** Converts the summary into an HTML page
    - **Output:** `.html` file
    - **Result:** Easy-to-read HTML summary of the transcript and its key points

### Summary of Outputs

- **Audio Extraction:** `.audio.mp3` file (isolated audio)
- **Audio Compression:** `.compressed_audio.mp3` file (compressed audio)
- **Transcript Extraction:** `.transcript.json` & `.transcript.txt` files (full text transcript)
- **Summarization:** `.summaries.json` file (key points and structured summaries)
- **Word Cloud Generation:** `.wordcloud.png` file (visual word cloud)
- **HTML Summary:** `.html` file (readable summary page)