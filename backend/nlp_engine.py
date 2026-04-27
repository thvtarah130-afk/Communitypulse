import spacy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spacy model 'en_core_web_sm' not found. Ensure you run: python -m spacy download en_core_web_sm. NLP features will use fallback.")
    nlp = None

def extract_insights(text: str):
    if not nlp:
        return {"entities": [], "summary": text[:100] + "..."}
        
    doc = nlp(text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    return {"entities": entities, "summary": text[:100] + "..."}

def categorize_issue(text: str) -> str:
    # Naive categorization using keywords
    text = text.lower()
    if any(word in text for word in ["doctor", "health", "medical", "hospital", "sick", "injury", "medicine"]):
        return "health"
    elif any(word in text for word in ["food", "hunger", "starving", "groceries", "water", "ration"]):
        return "food"
    elif any(word in text for word in ["school", "education", "teach", "learn", "student", "books"]):
        return "education"
    elif any(word in text for word in ["road", "bridge", "building", "infrastructure", "electricity", "power", "water pipe"]):
        return "infrastructure"
    return "other"
