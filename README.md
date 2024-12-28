# Reddit Sentiment and Trend Analysis

This project is a real-time sentiment and trend analysis program for Reddit comments and submissions. It allows users to analyze Reddit data based on specific keywords (for sentiment analysis) or general trends in the latest posts (for trend analysis).

## Table of Contents
- [Credits](#credits)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#how-to-run)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgements)

## Credits
This project was created by [<b>Harshal Gunjal</b>](https://github.com/HarshalGunjalOp) (`HarshalGunjalOp`) and [<b>Iftikar Alam</b>](https://github.com/iftikar0016) (`iftikar0016`).

## Features
- **Sentiment Analysis**: Analyze Reddit comments containing specific keywords and classify them as positive, negative, or neutral based on sentiment polarity.
- **Trend Analysis**: Analyze trends in Reddit submissions using topic modeling (via BERTopic).
- **Real-Time Data Fetching**: Fetch Reddit data in real-time using the Reddit API with the `praw` library.
- **Database Integration**: Store Reddit comments and submissions in an SQLite database for persistent storage.

## Requirements
To run this project, you'll need the following libraries and tools installed:
- Python 3.x
- `praw` for accessing Reddit data.
- `nltk` for sentiment analysis (VADER).
- `pandas` for data manipulation.
- `spacy` for text preprocessing.
- `sentence-transformers` for embeddings used in BERTopic.
- `bertopic` for trend analysis.
- `sqlite3` for database integration.

You can install the required libraries using the provided environment file.

## Installation

If you are using conda, you can set up your environment using the `environment.yml` file:

```bash
conda env create -f environment.yml
conda activate <your_environment_name>
```

Alternatively, you can install the dependencies manually using pip:

```bash
pip install -r requirements.txt
```

Additionally, download the necessary NLP models:
```bash
python -m spacy download en_core_web_sm
```

## How to Run

1) Clone the repository:

```bash
git clone https://github.com/HarshalGunjalOp/Reddit-Sentiment-And-Trend-Analysis
cd Reddit-Sentiment-And-Trend-Analysis
```

2) Set up the environment: If you're using Conda:

```bash
conda env create -f environment.yml
conda activate reddit-sentiment-and-trend-analysis
```

3) Run the program: To start the program, simply run the main.py file:

```bash
python main.py
```

4) The program will prompt you to choose between :

- Option 1 : Search for a keyword and analyze the sentiment of Reddit comments.
- Option 2 : Analyze trends in the latest Reddit comments.
- Option 3 : Exit the program.

5) <B>Database Usage</B> : The program uses an SQLite database (sqlite.db) to store fetched comments and submissions. Ensure the database is accessible in the project directory. If needed, you can inspect and query the database using SQLite tools.

## Contributing

Feel free to open issues or pull requests if you find bugs or have suggestions for improvements.

## License

This project is licensed under the `MIT License`. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project uses the Reddit API and the `praw` library for accessing Reddit data.
- The sentiment analysis is powered by the `nltk` library and the VADER sentiment analyzer.
- The trend analysis is performed using BERTopic.
- The SQLite database is used for persistent storage.

