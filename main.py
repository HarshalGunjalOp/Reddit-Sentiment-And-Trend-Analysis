import time
import sqlite3

while True:
    print("\n\nStarting the program...")
    print("Select an option:")
    print("1. Search for a keyword and analyse the sentiment of reddit comments")
    print("2. Analyze trends in the latest reddit comments")
    print("3. Exit")
    option = input("Enter your choice (1/2/3): ")

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

    if option == '1':
        # For sentiment analysis, prompt for a keyword and subreddit
        keyword = input("Enter a keyword to search for: ")
        subreddit_name = input("Enter the subreddit name (default='all'): ") or 'all'
        
        import analytics.fetch
        # Fetch comments containing the keyword
        comments = analytics.fetch.search_keyword_in_comments_of_latest_posts(keyword, subreddit_name)
        
        if comments:
            print(f"Found {len(comments)} comments containing '{keyword}'.")
            
            # Save comments to the database
            import sqlite3
            conn = sqlite3.connect('sqlite.db')
            cursor = conn.cursor()
            
            for comment in comments:
                cursor.execute(
                    "INSERT OR IGNORE INTO comments (id, comment, created_at) VALUES (?, ?, ?)",
                    (str(comment.id), comment.body, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment.created_utc)))
                )
            conn.commit()
            
            # Call sentiment analysis logic
            import analytics.sentiment
            print("Sentiment analysis complete.")
            
        else:
            print(f"No comments found containing '{keyword}'.")

    elif option == '2':
        # For trend analysis, fetch the latest comments
        subreddit_name = input("Enter the subreddit name (default='all'): ") or 'all'
        
        import analytics.fetch
        # Fetch the latest comments
        comments = analytics.fetch.get_latest_comments_from_subreddit(subreddit_name)
        
        if comments:
            print(f"Found {len(comments)} latest comments.")
            
            # Save comments to the database (this could be handled the same way as sentiment)
            import sqlite3
            conn = sqlite3.connect('sqlite.db')
            cursor = conn.cursor()
            
            for comment in comments:
                cursor.execute(
                    "INSERT OR IGNORE INTO comments (id, comment, created_at) VALUES (?, ?, ?)",
                    (str(comment.id), comment.body, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment.created_utc)))
                )
            conn.commit()
            
            # Call trend analysis logic
            import analytics.trend
            print("Trend analysis complete.")
            
        else:
            print("No comments found for trend analysis.")

    elif option == '3':
        print("Exiting the program...")
        break

    else:
        print("Invalid option. Please try again.")
