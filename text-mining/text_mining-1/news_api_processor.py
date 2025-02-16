import json
import pandas as pd
from collections import defaultdict
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

def process_news_api_data(json_file):
    """
    Process News API JSON data to create a word frequency matrix.
    
    Args:
        json_file (str): Path to the News API JSON file
        
    Returns:
        pd.DataFrame: Word frequency matrix with news sources as rows and words as columns
    """
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Initialize word frequency dictionary for each source
    source_word_freq = defaultdict(lambda: defaultdict(int))
    
    # Download required NLTK data if not already present
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')
    
    # Get stop words and punctuation for cleaning
    stop_words = set(stopwords.words('english'))
    
    # Process each article
    for article in data['articles']:
        source_name = article['source']['name'].replace('/', '_').replace(' ', '_')
        
        # Combine all text content
        text_content = []
        if article.get('title'):
            text_content.append(article['title'])
        if article.get('description'):
            text_content.append(article['description'])
        if article.get('content'):
            text_content.append(article['content'])
        
        # Join all text content
        full_text = ' '.join(text_content)
        
        # Clean and tokenize text
        # Remove URLs
        full_text = re.sub(r'http\S+|www\S+|https\S+', '', full_text, flags=re.MULTILINE)
        # Remove special characters and digits
        full_text = re.sub(r'[^\w\s]', ' ', full_text)
        full_text = re.sub(r'\d+', '', full_text)
        # Convert to lowercase
        full_text = full_text.lower()
        
        # Tokenize
        words = word_tokenize(full_text)
        
        # Count word frequencies (excluding stop words and empty strings)
        for word in words:
            if word and word not in stop_words and len(word) > 1:
                source_word_freq[source_name][word] += 1
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(source_word_freq, orient='index')
    
    # Fill NaN values with 0
    df = df.fillna(0)
    
    # Save to CSV
    output_file = json_file.replace('.json', '_corpus.csv')
    df.to_csv(output_file)
    
    print(f"Processed {len(data['articles'])} articles from {len(df)} unique sources")
    print(f"Found {len(df.columns)} unique words")
    print(f"Output saved to: {output_file}")
    
    return df

if __name__ == "__main__":
    # Example usage
    # df = process_news_api_data('./data/news_api_climate_change.json')
