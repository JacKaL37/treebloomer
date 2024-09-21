import json
import os
from pathlib import Path
from jinja2 import Template
import markdown2
import logging

logger = logging.getLogger(__name__)

def generate_html_summary(input_file: Path, subfolder: Path) -> Path:
    logger.info(f"Generating HTML summary for {input_file.stem}...")
    
    original_stem = input_file.stem.rsplit('.', 1)[0]
    output_file = subfolder / f"{original_stem}.html"
    
    if output_file.exists():
        logger.info(f"HTML summary file {output_file} already exists. Skipping generation.")
        return output_file
    
    try:
        # Read the JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert markdown to HTML
        markdowner = markdown2.Markdown()
        page_summary_html = markdowner.convert(data['page_summary'])
        
        # Prepare the data for the template
        context = {
            'title': original_stem,
            'sentence_summary': data['sentence_summary'],
            'topics': data['topics'],
            'keywords': data['keywords'],
            'paragraph_summary': data['paragraph_summary'],
            'page_summary': page_summary_html,
            'pull_quotes': data['pull_quotes'],
            'video_filename': f"../{original_stem}.mp4", 
            'model': data['llm_details']['model'],
            'temperature': data['llm_details']['temperature'],
            'system_prompt': data['llm_details']['system_prompt'],
            'output_schema': json.dumps(data['llm_details']['output_json_schema'], indent=2),
        }
        
        # HTML template
        template = Template('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            line-height: 1.6; 
            color: #FFFFFF; 
            background-color: #000000; 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .container { display: flex; flex-wrap: wrap; gap: 20px; }
        .full-width { width: 100%; }
        .column { flex: 1; min-width: 300px; }
        h1 { color: #FF00FF; /* Magenta */ }
        h2 { color: #00FFFF; /* Cyan */ }
        .topics, .keywords { background-color: #4B0082; /* Indigo */ padding: 10px; border-radius: 5px; }
        .topics span, .keywords span { 
            display: inline-block; 
            margin-right: 10px; 
            background-color: #DE3163; /* Cerise */ 
            color: white; 
            padding: 2px 8px; 
            border-radius: 3px; 
        }
        .pull-quote { 
            background-color: #4B0082; /* Indigo */
            padding: 10px; 
            margin: 10px 0; 
            border-radius: 5px; 
            font-style: italic; 
        }
        .summary { background-color: #1A1A1A; padding: 15px; border-radius: 5px; }
        #togglePrompt { cursor: pointer; color: #00FFFF; /* Cyan */ }
        pre { 
            background-color: #1A1A1A; 
            padding: 10px; 
            border-radius: 5px; 
            overflow-x: auto; 
            color: #FFFFFF; 
        }
                            
        code {
            background-color: #111111;
            padding: 2px 4px;
            border-radius: 3px;
            color: #DE3163
        }
                            
        #promptDetails {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.5s ease-out, opacity 0.5s ease-out;
            opacity: 0;
        }

        #promptDetails.show {
            max-height: 2000px; /* Adjust this value based on your content */
            transition: max-height 0.5s ease-in, opacity 0.5s ease-in;
            opacity: 1;
        }

        .video-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
        }

        .video-container video {
            max-width: 80%;
            height: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="full-width">
            <h1>{{ title }}</h1>
            <p id="togglePrompt"><small>as summarized by </small><code>{{ model }}</code><small> at temperature </small><code>{{ temperature }}</code></p>
            <div id="promptDetails">
                <h3>System Prompt:</h3>
                <pre>{{ system_prompt }}</pre>
                <h3>Output Schema:</h3>
                <pre>{{ output_schema }}</pre>
            </div>
            <div class="video-container">
                <video width="100%" controls>
                    <source src="{{ video_filename }}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            <p><strong>{{ sentence_summary }}</strong></p>
            
            <p class="topics">
                <strong>Topics:</strong><br/>
                <small>
                {% for topic in topics %}
                <span>{{ topic }}</span>
                {% endfor %}
                </small>
            </p>
        </div>
        
        <div class="column">
            <h2>Abstract</h2>
            <p>{{ paragraph_summary }}</p>
            
            <p class="keywords">
                <strong>Keywords:</strong><br/>
                <small>
                {% for keyword in keywords %}
                <span>{{ keyword }}</span>
                {% endfor %}
                </small>
            </p>
        </div>
        
        <div class="column">
            <div class="summary">
            {{ page_summary | safe }}
            </div>
        </div>
    </div>

    <script>
        document.getElementById('togglePrompt').addEventListener('click', function() {
            var details = document.getElementById('promptDetails');
            details.classList.toggle('show');
        });
    </script>
</body>
</html>
        ''')
        
        # Render the template
        html_content = template.render(context)
        
        # Write the HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Generated HTML summary at {output_file}.")
        return output_file
    except Exception as e:
        logging.error(f"Failed to generate HTML summary for {input_file}: {e}")
        if output_file.exists():
            output_file.unlink()
        raise
