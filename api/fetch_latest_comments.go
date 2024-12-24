package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "net/url"
    "os"
    "strings"
    "time"

    "github.com/joho/godotenv"
)

// CommentData represents a single comment's relevant fields in Reddit's JSON response.
type CommentData struct {
    Body      string  `json:"body"`
    CreatedUTC float64 `json:"created_utc"`
}

// Child encapsulates a single comment object in Reddit's JSON.
type Child struct {
    Kind string `json:"kind"`
    Data CommentData `json:"data"`
}

// ListingData is the "data" structure of the listing response, containing an array of children.
type ListingData struct {
    Children []Child `json:"children"`
}

// ListingResponse is the top-level structure for the subreddit comments.json response.
type ListingResponse struct {
    Kind string `json:"kind"`
    Data ListingData `json:"data"`
}

func main() {
    // Load environment variables from .env file
    err := godotenv.Load(".env")
    if err != nil {
        log.Println("Warning: Could not load .env file. Make sure environment variables are set.")
    }

    clientID := os.Getenv("CLIENT_ID")
    clientSecret := os.Getenv("CLIENT_SECRET")
    userAgent := os.Getenv("USER_AGENT")

    if clientID == "" || clientSecret == "" || userAgent == "" {
        log.Fatal("CLIENT_ID, CLIENT_SECRET, or USER_AGENT not set in environment")
    }

    // Prompt user for inputs
    var keyword string
    var subreddit string

    fmt.Print("Enter a keyword to search for: ")
    fmt.Scanln(&keyword)

    fmt.Print("Enter the subreddit name (default='all'): ")
    fmt.Scanln(&subreddit)
    if subreddit == "" {
        subreddit = "all"
    }

    // Obtain OAuth2 token
    token, err := getRedditToken(clientID, clientSecret, userAgent)
    if err != nil {
        log.Fatalf("Error fetching Reddit token: %v\n", err)
    }

    start := time.Now()

    // Fetch comments (limit=1000)
    limit := 1000
    comments, err := fetchLatestComments(subreddit, limit, token, userAgent)
    if err != nil {
        log.Fatalf("Error fetching comments: %v\n", err)
    }

    // Filter and print comments containing the keyword
    found := false
    for _, c := range comments {
        if strings.Contains(c.Data.Body, keyword) {
            found = true
            // Convert created_utc to Go time.Time (UTC)
            utcSeconds := int64(c.Data.CreatedUTC)
            commentTime := time.Unix(utcSeconds, 0).UTC()

            fmt.Printf("%s | %s\n\n", commentTime.Format(time.RFC3339), c.Data.Body)
        }
    }

    if !found {
        fmt.Printf("No comments containing '%s' found.\n", keyword)
    }

    duration := time.Since(start)
    fmt.Printf("Execution time: %.2f seconds\n", duration.Seconds())
}

// getRedditToken performs OAuth2 client credentials flow and returns an access token.
func getRedditToken(clientID, clientSecret, userAgent string) (string, error) {
    /*
       Reddit's OAuth2 token endpoint: https://www.reddit.com/api/v1/access_token
       We need to send a POST request with:
         - grant_type: client_credentials
         - Basic Auth using clientID and clientSecret
         - User-Agent header
    */

    endpoint := "https://www.reddit.com/api/v1/access_token"
    data := url.Values{}
    data.Set("grant_type", "client_credentials")

    req, err := http.NewRequestWithContext(context.Background(), http.MethodPost, endpoint, strings.NewReader(data.Encode()))
    if err != nil {
        return "", err
    }
    req.SetBasicAuth(clientID, clientSecret)
    req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
    req.Header.Set("User-Agent", userAgent)

    client := &http.Client{
        Timeout: 15 * time.Second,
    }
    resp, err := client.Do(req)
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return "", fmt.Errorf("bad response code: %d", resp.StatusCode)
    }

    var result map[string]interface{}
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return "", err
    }

    token, ok := result["access_token"].(string)
    if !ok {
        return "", fmt.Errorf("could not parse access_token from response")
    }

    return token, nil
}

// fetchLatestComments fetches the latest comments from a subreddit using the OAuth2 token.
func fetchLatestComments(subreddit string, limit int, token string, userAgent string) ([]Child, error) {
    // Example endpoint: https://oauth.reddit.com/r/<subreddit>/comments.json?limit=1000
    endpoint := fmt.Sprintf("https://oauth.reddit.com/r/%s/comments.json?limit=%d", subreddit, limit)

    req, err := http.NewRequestWithContext(context.Background(), http.MethodGet, endpoint, nil)
    if err != nil {
        return nil, err
    }
    req.Header.Set("Authorization", "bearer "+token)
    req.Header.Set("User-Agent", userAgent)

    client := &http.Client{
        Timeout: 15 * time.Second,
    }
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("fetchComments got status code: %d", resp.StatusCode)
    }

    var listingResp ListingResponse
    if err := json.NewDecoder(resp.Body).Decode(&listingResp); err != nil {
        return nil, err
    }

    // listingResp.Data.Children should hold an array of comments
    return listingResp.Data.Children, nil
}
