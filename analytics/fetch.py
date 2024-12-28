import praw
import time
import sqlite3

# Initialize the Reddit client
reddit = praw.Reddit(
        client_id='NNTlbq_GJlrUXwOCw5TC2Q',
        client_secret='vNcIczNFXXpIe0G2WEPfWdpL9SJt0Q',
        user_agent='realtime-analysis-and-prediction-dashboard-for-social-media-data'
)

def search_keyword_in_comments_of_latest_posts(keyword, subreddit_name='all', limit=1000):
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

def get_latest_comments_from_subreddit(subreddit_name='all', limit=1000):
    """
    Fetches the latest comments from a subreddit.
    :param subreddit_name: The name of the subreddit.
    :param limit: How many of the latest comments to fetch (default=100).
    :return: A list of comments.
    """
    comments = []
    for comment in reddit.subreddit(subreddit_name).comments(limit=limit):
        comments.append(comment)
        
    return comments

def get_latest_submissions_from_subreddit(subreddit_name='all', limit=1000):
    """
    Fetches the latest submissions from a subreddit.
    :param subreddit_name: The name of the subreddit.
    :param limit: How many of the latest submissions to fetch (default=100).
    :return: A list of submissions.
    """
    submissions = []
    for submission in reddit.subreddit(subreddit_name).new(limit=limit):
        submissions.append(submission)

    return submissions
    

if __name__ == "__main__":
    start = time.time()
    
    # Connect to the SQLite database
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id TEXT PRIMARY KEY,
        comment TEXT,
        created_at TEXT
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id TEXT PRIMARY KEY,
        submission TEXT,
        created_at TEXT
    );
    """)
    conn.commit()
    
    # keyword = input("Enter a keyword to search for: ")
    # subreddit_name = input("Enter the subreddit name (default='all'): ")
    # comments_with_keyword = search_keyword_in_comments_of_latest_posts(keyword, subreddit_name, 1000)
    # if comments_with_keyword:
    #     print(f"Comments containing '{keyword}':", len(comments_with_keyword))
    # else:
    #     print(f"No comments containing '{keyword}' found.")
    
    
    # subreddit_name = input("Enter the subreddit name (default='all'): ")
    # comments = get_latest_comments_from_subreddit(subreddit_name, 1000)
    # if comments:
    #     for comment in comments:
    #         if "*I am a bot" in comment.body:
    #             continue
    #         cursor.execute(
    #             "INSERT OR IGNORE INTO comments (id, comment, created_at) VALUES (?, ?, ?)",
    #             (str(comment.id), comment.body, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment.created_utc)))
    #         )
    #         conn.commit()
    #         print(f"Comment: {comment.body}")
    # else:
    #     print(f"No comments found.")
    
    # submissions = get_latest_submissions_from_subreddit(subreddit_name, 1000)
    # if submissions:
    #     for submission in submissions:
    #         if "*I am a bot" in submission.selftext:
    #             continue
    #         cursor.execute(
    #             "INSERT OR IGNORE INTO submissions (id, submission, created_at) VALUES (?, ?, ?)",
    #             (str(submission.id), submission.selftext, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(submission.created_utc)))
    #         )
    #         conn.commit()
    #         print(f"Submission: {submission.selftext}")
    # else:
    #         print(f"No submissions found.")
        
    end = time.time()
    print(f"Execution time: {end - start} seconds")
    
    

    