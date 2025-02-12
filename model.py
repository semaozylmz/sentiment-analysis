from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = LogisticRegression()
        self._train_model()

    def _train_model(self):
        # Simplified training data for demonstration
        positive_samples = [
            "harika bir deneyimdi",
            "çok beğendim",
            "muhteşem",
            "çok güzel",
            "başarılı"
        ]
        negative_samples = [
            "berbat",
            "hiç beğenmedim",
            "kötü bir deneyim",
            "çok kötü",
            "başarısız"
        ]

        X = positive_samples + negative_samples
        y = [1] * len(positive_samples) + [0] * len(negative_samples)

        # Fit vectorizer and transform training data
        X_vectorized = self.vectorizer.fit_transform(X)
        
        # Train model
        self.model.fit(X_vectorized, y)

    def predict(self, text):
        # Vectorize input text
        text_vectorized = self.vectorizer.transform([text])
        
        # Get prediction probability
        proba = self.model.predict_proba(text_vectorized)[0]
        
        # Get sentiment class
        sentiment = "positive" if proba[1] > 0.5 else "negative"
        
        # Return sentiment and confidence
        return sentiment, max(proba)
