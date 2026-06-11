from textblob import TextBlob
import re
from typing import List, Tuple, Dict
from typing import List, Dict
from textblob import TextBlob
import re

def extract_key_phrases(text: str, top_n: int = 10) -> List[str]:
    """Extract key phrases using NLP"""
    blob = TextBlob(text)
    phrases = blob.noun_phrases
    return list(set(phrases))[:top_n]

def analyze_sentiment(text: str) -> Dict[str, float]:
    """Analyze sentiment of text"""
    blob = TextBlob(text)
    return {
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity
    }

def extract_entities(text: str) -> List[Dict[str, str]]:
    """Extract named entities (simplified)"""
    # Note: For production, use spaCy or similar
    blob = TextBlob(text)
    entities = []
    for np in blob.noun_phrases:
        entities.append({"entity": str(np), "type": "noun_phrase"})
    return entities[:20]

def calculate_readability(text: str) -> Dict[str, float]:
    """Calculate readability scores"""
    sentences = text.split('.')
    words = text.split()
    if not sentences or not words:
        return {"flesch_score": 0, "grade_level": 0}
    
    avg_words_per_sentence = len(words) / len(sentences)
    avg_syllables_per_word = sum(1 for word in words if len(word) > 3) / len(words)
    
    # Simplified Flesch Reading Ease
    flesch = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
    
    return {
        "flesch_score": max(0, min(100, flesch)),
        "grade_level": max(1, min(12, int((flesch - 80) / 10) + 5))
    }