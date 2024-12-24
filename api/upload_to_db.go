package upload

import (
  "database/sql"
  "encoding/json"
  "fmt"

  "/fetch_latest_comments.go"
)

// Comment represents a comment to be stored in the database
type Comment struct {
  Body       string  `json:"body"`
  CreatedUTC int64   `json:"created_utc"`
  CommentTime time.Time `json:"-"` // Not included in JSON
}

// upload_comments_to_db takes comments data and a database path as arguments and stores them in an SQLite database
func upload_comments_to_db(comments []fetch_latest_comments_api.Child, dbPath string) error {
  db, err := sql.Open("sqlite3", dbPath)
  if err != nil {
    return fmt.Errorf("error opening database: %w", err)
  }
  defer db.Close()

  // Create table if it doesn't exist (adjust schema if needed)
  _, err = db.Exec(`CREATE TABLE IF NOT EXISTS comments (
    body TEXT NOT NULL,
    created_utc INTEGER NOT NULL,
    comment_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
  )`)
  if err != nil {
    return fmt.Errorf("error creating table: %w", err)
  }

  stmt, err := db.Prepare("INSERT INTO comments (body, created_utc) VALUES (?, ?)")
  if err != nil {
    return fmt.Errorf("error preparing statement: %w", err)
  }
  defer stmt.Close()

  for _, comment := range comments {
    commentTime := time.Unix(int64(comment.Data.CreatedUTC), 0).UTC()
    convertedComment := Comment{
      Body:       comment.Data.Body,
      CreatedUTC: int64(comment.Data.CreatedUTC),
      CommentTime: commentTime,
    }

    jsonData, err := json.Marshal(convertedComment)
    if err != nil {
      return fmt.Errorf("error marshalling comment data: %w", err)
    }

    // Uncomment this line if you want to see the data being inserted (for debugging)
    // fmt.Println(string(jsonData)) 

    _, err = stmt.Exec(jsonData, convertedComment.CreatedUTC)
    if err != nil {
      return fmt.Errorf("error inserting comment: %w", err)
    }
  }

  return nil
}