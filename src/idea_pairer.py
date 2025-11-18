import pandas as pd
import random
import re
import spacy
from sklearn.feature_extraction.text import TfidVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords


nlp = spacy.load("en_core_web_sm")
STOPWORDS = set(stopwords.words("english"))


def clean_text(text):
    """ Simple Cleaning for headline """
    if not isinstance(text, str):
        return ""
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = text.lower()
    return text


def extract_keywords(text, top_n=5):
    """ Extract noun chunks or keywords using Spacy """
    doc = nlp(text)
    keywords = [chunk.text for chunk in doc.noun_chunks if chunk.text.lower() not in STOPWORDS]
    return keywords[:top_n]


def load_news(filepath):
    """ Load the news """
    df = pd.read_csv(filepath)
    df["cleaned"] = df["title"].apply(clean_text)
    return df


def compute_distance_matrix(texts):
    """ Compute pair-wise cosine similarity (lower = more novel pairing) """
    vectorizer = TfidVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(texts)
    sim_matrix = cosine_similarity(tfidf)
    return 1 - sim_matrix   #distance = inverse of similarity


def generate_random_pairs(df, n_pairs=5):
    """ Generate pairs of distant topics """
    distances = compute_distance_matrix(df["cleaned"].tolist())
    pairs = []
    for _ in range(n_pairs):
        i, j = random.sample(range(len(df)), 2)
        pairs.append({
            "topic_a": df.iloc[i]["title"],
            "topic_b": df.iloc[j]["title"],
            "distance": round(distances[i][j], 2)
        })
    
    #sort by most distant
    pairs.sort(key=lambda x: x["distance"], reverse=True)
    return pairs

if __name__ == "__main__":
    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d")
    df = load_news(f"date_{date_str}.csv")

    pairs = generate_random_pairs(df, n_pairs=5)
    for p in pairs:
        print(f"🌀 [{p['distance']}] {p['topic_a']} ↔ {p['topic_b']}")