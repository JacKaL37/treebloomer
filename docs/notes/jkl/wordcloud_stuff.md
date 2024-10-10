```python
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = [
            #    (222, 49, 99),  # Cerise
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


# Function to create and save the word cloud
def create_word_cloud(text, output_file, shape='rectangle', mask_path=None, random_state=42):

    # Add custom stopwords to the default STOPWORDS
    stopwords = set(STOPWORDS)
    custom_stopwords = {
        "the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", 
        "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", 
        "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", 
        "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", 
        "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "too", "very", "can", 
        "will", "just",
        "really","kind","lot","going","okay","one","even","link","now","let","way","might",
        "thing","want","sort","something","mean","number","things","well","idea","need","say","know",
        "right","see","word",
        "go","use","different","stuff","actually","little","time","make","work","two","look",
        "start","take","still","able",
    }
    stopwords.update(custom_stopwords)

    random.seed(random_state)

    # Define mask based on shape
    if shape == 'rectangle':
        mask = None
    elif shape == 'circle':
        x, y = np.ogrid[:1000, :1000]
        mask = (x - 500) ** 2 + (y - 500) ** 2 > 400 ** 2
        mask = 255 * mask.astype(int)
    elif shape == 'custom' and mask_path:
        mask = np.array(Image.open(mask_path))
    else:
        raise ValueError("Invalid shape or missing mask path for custom shape")

    wordcloud = WordCloud(width=1000, height=1000, 
                          background_color='black', 
                          stopwords=stopwords,
                          min_font_size=6,
                          max_font_size=10000,
                          color_func=color_func,
                          mask=mask,
                          random_state=random_state).generate(text)

    
    plt.figure(figsize=(10,10), facecolor='black')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    
    plt.savefig(output_file, bbox_inches='tight', facecolor='black')
    plt.close()
```

```json
{stopwords:[
"the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", 
"we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", 
"their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", 
"have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", 
"all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "too", "very", "can", 
"will", "just",
"really","kind","lot","going","okay","one","even","link","now","let","way","might",
"thing","want","sort","something","mean","number","things","well","idea","need","say","know",
"right","see","word",
"go","use","different","stuff","actually","little","time","make","work","two","look",
"start","take","still","able",
]}
```