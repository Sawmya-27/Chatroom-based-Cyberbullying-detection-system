# File: utils/file_utils.py

import joblib
import re
import string
from core.bullying_detector import detect_bullying_image

# Load stopwords
with open("/Users/sawmy/Desktop/img project/utils/stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f)

# Load classifier and vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
model = joblib.load("/Users/sawmy/Desktop/img project/utils/LinearSVC_0.pkl")
vocab = joblib.load("/Users/sawmy/Desktop/img project/utils/tfidf_vector_vocabulary_0.pkl")
vectorizer = TfidfVectorizer(vocabulary=vocab)
vectorizer.fit(["placeholder"])  # Dummy fit to initialize IDF


def is_bullying_content(path, content_type):
    if content_type == 'image':
        return detect_bullying_image(path)
    elif content_type == 'text':
        return is_bullying_text(path)
    else:
        return False

def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    words = text.split()
    words = [word for word in words if word not in stopwords]
    return " ".join(words)

def is_bullying_text(text):
    cleaned = clean_text(text)
    X = vectorizer.transform([cleaned])
    prediction = model.predict(X)
    return prediction[0] == 1
