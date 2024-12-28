import sqlite3
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# Connect to the database
conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

# Retrieve comments
cursor.execute("SELECT id, comment FROM comments")
rows = cursor.fetchall()

sia = SentimentIntensityAnalyzer()

sentiment_results = []

for row in rows:
    comment_id = row[0]
    comment_text = row[1]
    
    # Run VADER analysis
    scores = sia.polarity_scores(comment_text)
    
    # For example, you might categorize sentiment by the compound score:
    compound_score = scores['compound']
    if compound_score >= 0.05:
        sentiment_label = 'positive'
    elif compound_score <= -0.05:
        sentiment_label = 'negative'
    else:
        sentiment_label = 'neutral'
    
    sentiment_results.append((comment_id, sentiment_label, compound_score))

conn.close()


total=0
for i in sentiment_results:
    total+= i[2]

average=total/(len(sentiment_results))

if average >= 0.05:
    print('\n\nObserved sentiment is positive.')
elif average <= -0.05:
    print('\n\nObserved sentiment is negative.')
else:
    print('\n\nObserved sentiment is neutral.')