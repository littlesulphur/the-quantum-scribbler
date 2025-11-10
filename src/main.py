from news_fetcher import fetch_news

def main():
    print("Fetching today's top news headlines...")
    news_df = fetch_news(page_size=5)
    print(f"Fetched {len(news_df)} articles.")
    print(news_df[["title","source"]])

if __name__ == "__main__":
    main()

