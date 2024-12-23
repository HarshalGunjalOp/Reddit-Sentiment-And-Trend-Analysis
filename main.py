import praw
from prawcore.exceptions import ResponseException
import dotenv

reddit = praw.Reddit(
        client_id=dotenv.get_key('.env', 'CLIENT_ID'), 
        client_secret=dotenv.get_key('.env', 'CLIENT_SECRET'),
        username=dotenv.get_key('.env', 'USERNAME'),
        password=dotenv.get_key('.env', 'PASSWORD'),
        user_agent=dotenv.get_key('.env', 'USER_AGENT')
    )

def search_reddit(keyword, subreddit="all", limit=10):
    """
    Search for posts with a specific keyword on Reddit.

    :param keyword: The keyword to search for.
    :param subreddit: The subreddit to search in (default: all).
    :param limit: Number of posts to retrieve.
    :return: A list of posts with title, URL, and subreddit.
    """
    results = []
    for submission in reddit.subreddit(subreddit).search(keyword, limit=limit):
        results.append({
            "title": submission.title,
            "url": submission.url,
            "subreddit": submission.subreddit.display_name,
            "created_utc": submission.created_utc
        })
    return results

# Step 3: Fetch recent posts
keyword = "machine learning"  # Replace with your keyword
posts = search_reddit(keyword, limit=5)

# Step 4: Display results
for post in posts:
    print(f"Title: {post['title']}")
    print(f"URL: {post['url']}")
    print(f"Subreddit: {post['subreddit']}")
    print(f"Posted on: {post['created_utc']}")
    print("-" * 50)
    
# try:
#     reddit = praw.Reddit(
#         client_id='NNTlbq_GJlrUXwOCw5TC2Q',
#         client_secret='vNcIczNFXXpIe0G2WEPfWdpL9SJt0Q',  # Removed whitespace
#         username='Diablo_The_Dark_Lord',
#         password='umaU5WW_.39bRU5',
#         user_agent='realtime-analysis-and-prediction-dashboard-for-social-media-data'
#     )

#     # Test with read-only access first
#     reddit.read_only = True
    
#     subreddit = reddit.subreddit('typing')
#     for post in subreddit.hot(limit=5):
#         print(post.title)

# except ResponseException as e:
#     print(f"Authentication Error: {e}")
# except Exception as e:
#     print(f"Error: {e}")
    
