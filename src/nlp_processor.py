import nltk
import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


class NLPProcessor:
    """Handles basic NLP preprocessing for database requirements."""

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

    def preprocess_text(self, text):
        """Clean and preprocess the input requirement."""

        # Convert text to lowercase
        text = text.lower()

        # Remove special characters and numbers
        text = re.sub(r"[^a-zA-Z\s]", "", text)

        # Tokenize the text
        tokens = word_tokenize(text)

        # Remove stopwords and lemmatize
        processed_tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words and len(token) > 2
        ]

        return processed_tokens