import re
from typing import List, Dict

def extract_key_phrases(text: str, top_n: int = 10) -> List[str]:
    """Extract key phrases without TextBlob"""
    # Simple keyword extraction
    words = text.lower().split()
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'that', 'this', 'these', 'those', 'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'under', 'over'}
    
    # Filter out stop words and short words
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    
    # Count frequencies
    from collections import Counter
    freq = Counter(keywords)
    
    # Return top_n keywords as phrases
    return [word for word, count in freq.most_common(top_n)]

def analyze_sentiment(text: str) -> Dict[str, float]:
    """Analyze sentiment without TextBlob"""
    positive_words = {
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'best', 'innovative', 
        'advanced', 'breakthrough', 'success', 'effective', 'powerful', 'positive', 
        'beneficial', 'exciting', 'promising', 'significant', 'important', 'valuable', 
        'helpful', 'improved', 'efficient', 'reliable', 'safe', 'easy', 'fast'
    }
    
    negative_words = {
        'bad', 'poor', 'worst', 'terrible', 'limited', 'failure', 'problem', 'issue', 
        'weak', 'ineffective', 'challenge', 'difficult', 'negative', 'harmful', 
        'dangerous', 'risky', 'concern', 'drawback', 'disadvantage', 'error', 'fail', 
        'broken', 'slow', 'hard', 'complex', 'expensive'
    }
    
    words = text.lower().split()
    pos_count = sum(1 for w in words if w in positive_words)
    neg_count = sum(1 for w in words if w in negative_words)
    
    # Calculate polarity (-1 to 1)
    total = pos_count + neg_count
    if total == 0:
        polarity = 0.0
    else:
        polarity = (pos_count - neg_count) / total
    
    # Simple subjectivity (based on sentiment word density)
    subjectivity = min(1.0, total / max(len(words), 1))
    
    return {
        "polarity": polarity,
        "subjectivity": subjectivity
    }

def extract_entities(text: str) -> List[Dict[str, str]]:
    """Extract named entities without TextBlob"""
    import re
    
    # Find capitalized words (potential entities)
    capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
    
    # Find acronyms (all caps)
    acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
    
    # Combine and remove duplicates
    all_entities = list(set(capitalized + acronyms))
    
    # Filter out common words
    common_words = {'The', 'And', 'For', 'With', 'This', 'That', 'These', 'Those', 'From', 'Have', 'Are', 'Was', 'Were'}
    entities = [e for e in all_entities if e not in common_words]
    
    # Return as dictionary list
    return [{"entity": entity, "type": "proper_noun"} for entity in entities[:20]]

def calculate_readability(text: str) -> Dict[str, float]:
    """Calculate readability scores without TextBlob"""
    # Split into sentences
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    words = text.split()
    
    if not sentences or not words:
        return {"flesch_score": 0, "grade_level": 0}
    
    # Calculate averages
    avg_words_per_sentence = len(words) / len(sentences)
    
    # Count syllables (simplified: count vowels)
    def count_syllables(word):
        word = word.lower()
        vowels = 'aeiou'
        count = 0
        prev_is_vowel = False
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_is_vowel:
                count += 1
            prev_is_vowel = is_vowel
        return max(1, count)
    
    total_syllables = sum(count_syllables(word) for word in words)
    avg_syllables_per_word = total_syllables / len(words)
    
    # Flesch Reading Ease formula
    flesch = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
    
    # Clamp to valid range
    flesch = max(0, min(100, flesch))
    
    # Estimate grade level
    grade_level = max(1, min(12, round((flesch - 80) / 10) + 5))
    
    return {
        "flesch_score": round(flesch, 2),
        "grade_level": grade_level
    }