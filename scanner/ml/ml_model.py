import re
import pickle
import os
from .preprocess import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = pickle.load(open(os.path.join(BASE_DIR, "scam_model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))

# strong scam keywords (override list)
STRONG_SCAM_PATTERNS = [
    r"registration fee",
    r"training fee",
    r"pay .* fee",
    r"after payment",
    r"no interview",
    r"immediate confirmation",
    r"100% placement",
    r"whatsapp",
    r"telegram",
]

def rule_based_override(text: str):
    text_l = text.lower()
    matched = []

    for pattern in STRONG_SCAM_PATTERNS:
        if re.search(pattern, text_l):
            matched.append(pattern)

    return matched


def predict_scam(text: str):
    cleaned = clean_text(text)

    # 1️⃣ ML prediction
    vec = vectorizer.transform([cleaned])
    prob = float(model.predict_proba(vec)[0][1])
    scam_prob_pct = round(prob * 100, 1)

    # 2️⃣ Rule-based override
    matched_rules = rule_based_override(text)

    if matched_rules:
        # FORCE scam if strong rules hit
        return (
            max(scam_prob_pct, 85.0),
            "High Risk Scam",
            f"Strong scam indicators detected: {', '.join(matched_rules)}"
        )

    # 3️⃣ Threshold-based decision
    if scam_prob_pct >= 80:
        return scam_prob_pct, "High Risk Scam", "High scam probability detected."
    elif scam_prob_pct >= 65:
        return scam_prob_pct, "Suspicious", "Some suspicious patterns detected."
    else:
        return scam_prob_pct, "Safe", "Below warning threshold. No strong scam indicators."
