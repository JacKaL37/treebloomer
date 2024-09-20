import json
import logging
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import colorsys
import random
import numpy as np
from PIL import Image
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords', quiet=True)

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = [
        (75, 0, 130),   # Indigo
        (0, 255, 255),  # Cyan
        (255, 0, 255),  # Magenta
    ]
    
    # Normalize the colors to [0, 1] range
    colors = [(r/255, g/255, b/255) for r, g, b in colors]
    
    # Use HSV color space for smooth transitions
    hsv_colors = [colorsys.rgb_to_hsv(*color) for color in colors]
    
    # Interpolate between colors based on font size
    t = (font_size - 10) / (100 - 10)  # Assuming font sizes range from 10 to 100
    t = max(0, min(t, 1))  # Clamp t between 0 and 1
    
    index = int(t * (len(hsv_colors) - 1))
    remainder = t * (len(hsv_colors) - 1) - index
    
    if index == len(hsv_colors) - 1:
        hsv = hsv_colors[-1]
    else:
        hsv1, hsv2 = hsv_colors[index], hsv_colors[index + 1]
        h = (1 - remainder) * hsv1[0] + remainder * hsv2[0]
        s = (1 - remainder) * hsv1[1] + remainder * hsv2[1]
        v = (1 - remainder) * hsv1[2] + remainder * hsv2[2]
        hsv = (h, s, v)
    
    rgb = colorsys.hsv_to_rgb(*hsv)
    return tuple(int(x * 255) for x in rgb)

def generate_word_cloud(input_file: Path, subfolder: Path) -> Path:
    logging.info(f"Generating word cloud for {input_file.stem}...")
    
    original_stem = input_file.stem.rsplit('.', 1)[0]
    output_file = subfolder / f"{original_stem}.wordcloud.png"
    
    if output_file.exists():
        logging.info(f"Word cloud file {output_file} already exists. Skipping generation.")
        return output_file
    
    try:
        # Read the transcript JSON
        with open(input_file, 'r') as file:
            transcript_data = json.load(file)
        
        # Extract the text from the transcript
        text = transcript_data['text']
        
        # Get the set of stopwords
        stop_words = set(stopwords.words('english'))
        custom_stop_words = {
            'um', 'uh', 'like', 'you know', 'I mean'
        }
        stop_words.update(custom_stop_words)
        
        # Generate the word cloud
        x, y = np.ogrid[:1000, :1000]
        mask = (x - 500) ** 2 + (y - 500) ** 2 > 400 ** 2
        mask = 255 * mask.astype(int)
        
        wordcloud = WordCloud(width=1000, height=1000, 
                              background_color='black', 
                              stopwords=stop_words,
                              min_font_size=6,
                              max_font_size=10000,
                              color_func=color_func,
                              mask=mask,
                              random_state=42).generate(text)
        
        # Display the generated image
        plt.figure(figsize=(10,10), facecolor='black')
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        
        # Save the image
        plt.savefig(output_file, bbox_inches='tight', facecolor='black')
        plt.close()
        
        logging.info(f"Generated word cloud at {output_file}.")
        return output_file
    except Exception as e:
        logging.error(f"Failed to generate word cloud for {input_file}: {e}")
        if output_file.exists():
            output_file.unlink()
        raise

