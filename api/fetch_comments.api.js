import dotenv from "dotenv";
import axios from "axios";
import readline from "readline";
import sqlite3 from "sqlite3";

// Load environment variables
dotenv.config();

// Configure input via command line
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

// Base URL for Reddit API
const BASE_URL = "https://oauth.reddit.com";

// Initialize SQLite database
const db = new sqlite3.Database('./db.sqlite', (err) => {
  if (err) {
    console.error("Error opening database:", err.message);
    process.exit(1);
  }
  console.log("Connected to the SQLite database.");
});

// Create comments table if it doesn't exist
db.run(`
  CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    comment TEXT,
    created_at TEXT
  )
`, (err) => {
  if (err) {
    console.error("Error creating table:", err.message);
    process.exit(1);
  }
});

// Authenticate and get an access token
async function getRedditToken() {
  const credentials = Buffer.from(
    `${process.env.CLIENT_ID}:${process.env.CLIENT_SECRET}`
  ).toString("base64");

  try {
    const response = await axios.post(
      "https://www.reddit.com/api/v1/access_token",
      "grant_type=client_credentials",
      {
        headers: {
          Authorization: `Basic ${credentials}`,
          "Content-Type": "application/x-www-form-urlencoded",
          "User-Agent": process.env.USER_AGENT,
        },
      }
    );

    return response.data.access_token;
  } catch (error) {
    console.error("Error fetching Reddit token:", error.response?.data || error.message);
    process.exit(1);
  }
}

// Fetch latest comments from a subreddit
async function fetchLatestComments(subreddit, limit, token) {
  try {
    const response = await axios.get(
      `${BASE_URL}/r/${subreddit}/comments.json?limit=${limit}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "User-Agent": process.env.USER_AGENT,
        },
      }
    );

    return response.data.data.children.map((child) => child.data);
  } catch (error) {
    console.error("Error fetching comments:", error.response?.data || error.message);
    process.exit(1);
  }
}

// Filter comments by keyword
function filterCommentsByKeyword(comments, keyword) {
  const lowerKeyword = keyword.toLowerCase();
  return comments.filter((comment) => comment.body && comment.body.toLowerCase().includes(lowerKeyword));
}

// Insert comments into the database
function insertCommentsIntoDB(comments) {
  const stmt = db.prepare("INSERT OR IGNORE INTO comments (id, text, created_at) VALUES (?, ?, ?)");
  db.serialize(() => {
    for (const comment of comments) {
      stmt.run(comment.id, comment.body, new Date(comment.created_utc * 1000).toISOString());
    }
    stmt.finalize((err) => {
      if (err) {
        console.error("Error finalizing statement:", err.message);
      } else {
        console.log(`Inserted ${comments.length} comments into the database.`);
      }
      db.close((err) => {
        if (err) {
          console.error("Error closing database:", err.message);
        } else {
          console.log("Database connection closed.");
        }
      });
    });
  });
}

// Main function
(async function main() {
  const token = await getRedditToken();

  rl.question("Enter a keyword to search for: ", async (keyword) => {
    rl.question("Enter the subreddit name (default='all'): ", async (subredditName) => {
      const subreddit = subredditName || "all";
      const limit = 1000;

      console.log(`\nSearching for comments containing '${keyword}' in '${subreddit}'...`);

      const startTime = Date.now();
      const comments = await fetchLatestComments(subreddit, limit, token);
      const matchingComments = filterCommentsByKeyword(comments, keyword);

      if (matchingComments.length > 0) {
        console.log(`\nComments containing '${keyword}':\n`);
        matchingComments.forEach((comment) => {
          const timestamp = new Date(comment.created_utc * 1000).toISOString();
          console.log(`${timestamp} | ${comment.body}\n`);
        });

        // Insert into DB
        insertCommentsIntoDB(matchingComments);
      } else {
        console.log(`\nNo comments containing '${keyword}' found.`);
        db.close((err) => {
          if (err) {
            console.error("Error closing database:", err.message);
          } else {
            console.log("Database connection closed.");
          }
        });
      }

      const endTime = Date.now();
      console.log(`\nExecution time: ${(endTime - startTime) / 1000} seconds`);

      rl.close();
    });
  });
})();
