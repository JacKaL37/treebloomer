Certainly! Using a JSON file for configuration is a great idea. Here's a sketch of what the config file might look like, followed by an example of how to implement it in the summarization step.

First, let's create a `config.json` file:

```json
{
  "summarization": {
    "model": "gpt-4-1106-preview",
    "temperature": 0.0,
    "system_prompt": "You are an expert summarizer and analyst. Your task is to read the attached transcript and provide various summaries.",
    "output_json_schema": {
      "type": "object",
      "properties": {
        "page_summary": {
          "type": "string",
          "description": "A concise but detailed short-form notes document summarizing the transcript..."
        },
        "paragraph_summary": {
          "type": "string",
          "description": "A concise summary of the transcript, at most a single paragraph."
        },
        "sentence_summary": {
          "type": "string",
          "description": "An extremely concise summary of the transcript, at most a single sentence."
        },
        "topics": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "An array of the major topics discussed as extracted from the transcript..."
        },
        "keywords": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "An array of field-appropriate keywords or search terms extracted from the transcript..."
        },
        "pull_quotes": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "An array of significant, memorable, or punchy quotes..."
        }
      },
      "required": ["page_summary", "paragraph_summary", "sentence_summary", "topics", "keywords", "pull_quotes"]
    }
  },
  "html_generation": {
    "template": "<!DOCTYPE html>...",
    "color_palette": {
      "background": "#000000",
      "text": "#FFFFFF",
      "heading": "#FF00FF",
      "subheading": "#00FFFF"
    }
  },
  "audio_compression": {
    "bitrate": "32k",
    "format": "mp3"
  },
  "process_control": {
    "skip": [],
    "force": []
  }
}
```

Now, let's modify the `summarize_transcript` function in `processes/summarization.py` to use this config:

```python
import json
from pathlib import Path
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def summarize_transcript(input_file: Path, subfolder: Path, force: bool = False) -> Path:
    config = load_config()
    summarization_config = config['summarization']
    
    process_name = 'summaries'
    
    logging.info(f"Summarizing transcript {input_file.stem}...")
    
    original_stem = input_file.stem.rsplit('.', 1)[0]
    output_file = subfolder / f"{original_stem}.{process_name}.json"
    
    if output_file.exists() and not force:
        logging.info(f"Summary file {output_file} already exists. Skipping summarization.")
        return output_file
    
    try:
        with open(input_file, 'r') as file:
            transcript_json = file.read()
            transcript_obj = json.loads(transcript_json)
            transcript_text = transcript_obj['text']
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=summarization_config['model'],
            temperature=summarization_config['temperature'],
            messages=[
                {"role": "system", "content": summarization_config['system_prompt']},
                {"role": "user", "content": f"Transcript:\n\n{transcript_text}"}
            ],
            response_format={"type": "json_object"},
            functions=[{"name": "output_json", "parameters": summarization_config['output_json_schema']}],
            function_call={"name": "output_json"}
        )
        
        summary_data = json.loads(response.choices[0].message.function_call.arguments)
        
        summary_data['llm_details'] = {
            'system_prompt': summarization_config['system_prompt'],
            'output_json_schema': summarization_config['output_json_schema'],
            'input_file': str(input_file),
            'input_file_stem': str(input_file.stem),
            'model': response.model,
            'temperature': summarization_config['temperature']
        }
        
        with open(output_file, 'w') as outfile:
            json.dump(summary_data, outfile, indent=4)
        
        logging.info(f"Summarized {input_file.stem} to {output_file}.")
        return output_file
    except Exception as e:
        logging.error(f"Failed to summarize {input_file}: {e}")
        if output_file.exists():
            output_file.unlink()
        raise
```

This implementation demonstrates how to:
1. Load the configuration from the JSON file.
2. Use the configuration values for the OpenAI API call.
3. Include the configuration details in the output for reference.

You can apply similar changes to other process functions, using the relevant sections of the config file. For the main script, you could load the config file at the start and pass the relevant parts to each function call.

This approach allows users to easily modify the behavior of the script without changing the code, making it more flexible and user-friendly.
