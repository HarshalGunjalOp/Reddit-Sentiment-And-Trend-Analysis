from bertopic import BERTopic
import sqlite3
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import spacy
from collections import Counter
from sentence_transformers import SentenceTransformer

# Connect to the SQLite database
conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

# Query to select relevant columns
query = "SELECT id, comment, created_at FROM comments"

# Read data into a pandas DataFrame
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Display the first few rows
# print(df.head())

# Load spaCy's English model
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
embedding_model = SentenceTransformer("all-distilroberta-v1")

def preprocess_text_spacy(text):
    if not isinstance(text, str):
        return ""
    # Lowercase the text
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove mentions and hashtags
    text = re.sub(r'\@\w+|\#', '', text)
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Process text with spaCy
    doc = nlp(text)
    
    # Lemmatize and remove stopwords
    tokens = [
        token.lemma_ for token in doc
        if token.is_alpha and not token.is_stop and len(token) > 2  # Remove short words
    ]
    
    return ' '.join(tokens)

# Apply preprocessing
df['clean_comment'] = df['comment'].apply(preprocess_text_spacy)

# Tokenize all comments
all_tokens = ' '.join(df['clean_comment']).split()
token_counts = Counter(all_tokens)

# Define thresholds
min_freq = 5  # Words appearing fewer times than this will be removed
max_freq = 0.95 * len(df)  # Words appearing in more than 95% of documents will be removed

# Identify tokens to keep
tokens_to_keep = {token for token, count in token_counts.items() if count >= min_freq and count <= max_freq}

# Filter tokens in each comment
df['clean_comment'] = df['clean_comment'].apply(lambda x: ' '.join([word for word in x.split() if word in tokens_to_keep]))


# # Display the first few cleaned comments
# print(df[['comment', 'clean_comment']].head())

# Initialize BERTopic
topic_model = BERTopic(
    language="english",
    verbose=True,
    nr_topics="auto",            # Let BERTopic determine the optimal number
    min_topic_size=5,            # Allow smaller topics to form
    embedding_model=embedding_model
)

# Fit BERTopic model
topics, probabilities = topic_model.fit_transform(df['clean_comment'])
df['topic'] = topics

# Handle probabilities dimensions
if probabilities.ndim == 1:
    df['probability'] = probabilities
    print("Probabilities are 1D. Each comment has a single probability value.")
elif probabilities.ndim == 2:
    df['probability'] = probabilities.max(axis=1)
    print("Probabilities are 2D. Max probability across topics assigned to each comment.")
else:
    raise ValueError(f"Unexpected number of dimensions in probabilities: {probabilities.ndim}")

# Get topic information
topic_info = topic_model.get_topic_info()
print("Number of Topics Identified (excluding Outliers):", topic_info.shape[0] - 1)
print(topic_info)
