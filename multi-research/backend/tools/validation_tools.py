# import re
# from typing import List, Tuple, Set

# def check_plagiarism_risk(text: str) -> Dict[str, float]:
#     """Check for potential plagiarism indicators"""
#     # Simplified check - in production use actual API
#     sentences = text.split('.')
#     common_phrases = {
#         "according to", "research shows", "studies indicate",
#         "it is important to note", "furthermore", "moreover"
#     }
    
#     risk_score = min(1.0, len([s for s in sentences if any(phrase in s.lower() for phrase in common_phrases)]) / len(sentences))
    
#     return {
#         "risk_score": risk_score,
#         "risk_level": "high" if risk_score > 0.7 else "medium" if risk_score > 0.3 else "low"
#     }

# def validate_citations(content: str) -> Dict[str, Any]:
#     """Validate that citations are properly formatted"""
#     citation_patterns = [
#         r'\[\d+\]',  # [1]
#         r'\([A-Za-z]+, \d{4}\)',  # (Author, 2024)
#         r'https?://[^\s]+'  # URLs
#     ]
    
#     citations_found = []
#     for pattern in citation_patterns:
#         citations_found.extend(re.findall(pattern, content))
    
#     return {
#         "total_citations": len(citations_found),
#         "citations": citations_found[:10],
#         "is_sufficient": len(citations_found) >= 3
#     }

# def check_consistency(text1: str, text2: str) -> float:
#     """Check consistency between two text versions"""
#     words1 = set(text1.lower().split())
#     words2 = set(text2.lower().split())
    
#     if not words1 or not words2:
#         return 0.0
    
#     intersection = words1.intersection(words2)
#     union = words1.union(words2)
    
#     return len(intersection) / len(union) if union else 0.0



from typing import Dict, List, Tuple, Set,Any
import re

def check_plagiarism_risk(text: str) -> Dict[str, float]:
    """Check for potential plagiarism indicators"""
    # Simplified check - in production use actual API
    sentences = text.split('.')
    common_phrases = {
        "according to", "research shows", "studies indicate",
        "it is important to note", "furthermore", "moreover"
    }
    
    risk_score = min(1.0, len([s for s in sentences if any(phrase in s.lower() for phrase in common_phrases)]) / len(sentences)) if sentences else 0
    
    return {
        "risk_score": risk_score,
        "risk_level": "high" if risk_score > 0.7 else "medium" if risk_score > 0.3 else "low"
    }

def validate_citations(content: str) -> Dict[str, Any]:
    """Validate that citations are properly formatted"""
    import re
    citation_patterns = [
        r'\[\d+\]',  # [1]
        r'\([A-Za-z]+, \d{4}\)',  # (Author, 2024)
        r'https?://[^\s]+'  # URLs
    ]
    
    citations_found = []
    for pattern in citation_patterns:
        citations_found.extend(re.findall(pattern, content))
    
    return {
        "total_citations": len(citations_found),
        "citations": citations_found[:10],
        "is_sufficient": len(citations_found) >= 3
    }

def check_consistency(text1: str, text2: str) -> float:
    """Check consistency between two text versions"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0