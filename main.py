import praw
from prawcore.exceptions import ResponseException
import dotenv
import time
import datetime

# Initialize the Reddit client
reddit = praw.Reddit(
    client_id=dotenv.get_key('.env', 'CLIENT_ID'),
    client_secret=dotenv.get_key('.env', 'CLIENT_SECRET'),
    user_agent=dotenv.get_key('.env', 'USER_AGENT')
)

def search_keyword_in_comments_of_latest_posts(keyword, subreddit_name='all', limit=10):
    """
    Searches for a given keyword in the comments of the latest posts in reddit.

    :param keyword: The keyword to search for.
    :param limit: How many of the latest submissions to analyze (default=10).
    :return: A list of comments that contain the keyword.
    """
    comments_with_keyword = []
    for comment in reddit.subreddit(subreddit_name).comments(limit=limit):
        if keyword in comment.body:
            comments_with_keyword.append(comment)
    return comments_with_keyword

if __name__ == "__main__":
    start = time.time()
    
    keyword = input("Enter a keyword to search for: ")
    subreddit_name = input("Enter the subreddit name (default='all'): ")
    comments_with_keyword = search_keyword_in_comments_of_latest_posts(keyword, subreddit_name, 1000)
    if comments_with_keyword:
        print(f"Comments containing '{keyword}':")
        for comment in comments_with_keyword:
            print(f"{ datetime.datetime.utcfromtimestamp(comment.created_utc)} {comment.body}\n\n")
    else:
        print(f"No comments containing '{keyword}' found.")
        
    end = time.time()
    print(f"Execution time: {end - start} seconds")
    
    

    
