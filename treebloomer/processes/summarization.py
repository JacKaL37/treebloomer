import logging
import json
from pathlib import Path
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: adjust this basic system prompt to be more specific. later, we'll abstract it to a config file.
# Pertinent information: 
# - current filename stem
# - artifact type (lecture video, podcast, etc.)
# - filetree (with "you are here")
#   - optional, in case you don't want any global awareness. 
system_prompt = """
You are an expert summarizer and analyst. Your task is to read the attached transcript and provide various summaries.

More details can be found in the output schema. 
"""

output_json_schema = {
  "type": "json_schema",
  "json_schema": {
    "name": "transcript_summary",
    "schema": {
      "type": "object",
      "properties": {
        "page_summary": {
          "type": "string",
          "description": "A concise but detailed short-form notes document summarizing the transcript, keeping the length of these notes between half a page and two pages. Uses a standard markdown document format (starting with a # heading), prioritizing concise bulleted lists of notes over full paragraphs to get more complete coverage. Does not include quotes, keywords, or topic lists, only an simple, structured summary of the content."
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
          "description": "An array of the major topics discussed as extracted from the transcript. These should be contained to specifically what content was covered to communicate to users what topics are discussed in the video."
        },
        "keywords": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "An array of field-appropriate keywords or search terms extracted from the transcript. These should be connective, helping users explore additional relevant information in the same vein as the content discussed. Prioritize generality with these keywords, like you might see in a research paper in an established domain."
        },
        "pull_quotes": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "An array of significant, memorable, or punchy quotes (best if all three!) that communicate core ideas or illustrate points, extracted VERBATIM* from the transcript. *(with the exception that the audio was highly compressed, so adjusting for obvious errors in transcription is acceptable."
        },
        # "llm_reflection": {
        #     "type": "string",
        #     "description": "A brief reflection from the LLM on its own summarization outputs, focusing on what worked, pain points, and what could be improved for a second round of summarization. The audience for this reflection is primarily other LLMs, though it should still be human readable."
        # }
      },
      "required": ["page_summary", "paragraph_summary", "sentence_summary", "topics", "keywords", "pull_quotes"],
      "additionalProperties": False
    },
    "strict": True
  }
}

model = "gpt-4o-2024-08-06"  # or another appropriate model
temperature = 0.0

logger = logging.getLogger(__name__)

def summarize_transcript(input_file: Path, subfolder: Path) -> Path:
    process_name = 'summaries'
    
    logger.info(f"Summarizing transcript {input_file.stem}...")
    
    original_stem = input_file.stem.rsplit('.', 1)[0]
    output_file = subfolder / f"{original_stem}.{process_name}.json"
    
    if output_file.exists():
        logger.info(f"Summary file {output_file} already exists. Skipping summarization.")
        return output_file
    
    try:
        # Read the transcript
        with open(input_file, 'r') as file:
            transcript_json = file.read()
            transcript_obj = json.loads(transcript_json)
            transcript_text = transcript_obj['text']
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model, 
            temperature = temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Transcript:\n\n{transcript_text}"}
            ],
            response_format=output_json_schema
        )
        
        # # TODO: Process the API response and extract the summary data
        summary_data = json.loads(response.choices[0].message.content)
        logger.info("summary_data: %s", summary_data)
        
        # # Add the prompt used to the summary data
        # summary_data['prompt_used'] = system_prompt
        summary_data['llm_details'] = {}
        summary_data['llm_details']['system_prompt'] = system_prompt
        summary_data['llm_details']['output_json_schema'] = output_json_schema
        summary_data['llm_details']['input_file'] = str(input_file)
        summary_data['llm_details']['input_file_stem'] = str(input_file)
        summary_data['llm_details']['model'] = response.model
        summary_data['llm_details']['temperature'] = temperature
        
        # Write the summary data directly to the output file
        with open(output_file, 'w') as outfile:
            json.dump(summary_data, outfile, indent=4)
        
        logger.info(f"Summarized {input_file.stem} to {output_file}.")
        return output_file
    except Exception as e:
        logging.error(f"Failed to summarize {input_file}: {e}")
        if output_file.exists():
            output_file.unlink()
        raise
