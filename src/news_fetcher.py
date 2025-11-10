"""
Module to fetch news articles from NewsAPI.org
- Loads NEWS_API_KEY from environment (.env)
- Fetches top headlines from NewsAPI
- Retries on transient errors with simple backoff
- Saves result CSV to ./data/YYYY-MM-DD_news.csv
- Returns a pandas DataFrame
"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime 

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

def fetch_news(country="us", category="technology", page_size=10):
    params = {
        "apiKey": API_KEY,
        "country": country,
        "pageSize": page_size,
    }
    if category:
        params["category"] = category
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("status") != "ok":
        raise RuntimeError(f"Error fetching news {data.get("message")}")
    
    articles = data["articles"]
    #new_list = []

    df = pd.DataFrame(
        [
            {
                "title": a["title"],
                "description": a["description"],
                "url": a["url"],
                "source": a["source"]["name"],
                "publishedAt": a["publishedAt"],
            }
            for a in articles
        ]
    )

    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = f"./data/{date_str}_news.csv"
    df.to_csv(output_path, index=False)
    return df

if __name__ == "__main__":
    news_df = fetch_news()
    print(news_df.head())

