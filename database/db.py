import sqlite3

def create_database(db_path='./db.sqlite'):
    # Connect to the SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table (example: a simple users table)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            comment TEXT,
            created_at TEXT
        );
    """)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database created (or already exists) at: {db_path}")

if __name__ == '__main__':
    create_database()
