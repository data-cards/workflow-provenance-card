
import re
import sklearn

from src.consts import *


STOPWORDS = {"the", "a", "an", "is", "are", "was", "were", "in", "of", "to", "and", "or", "it", "this", "that", "with", "for", "on", "at", "by", "from", "as", "be", "has", "have", "its"}


# ---------------------------------------------------------------------------
# 1. FACTUAL COVERAGE SCORE
# ---------------------------------------------------------------------------

def coverage_score(total_card: str, question: str, answer : str) -> dict:
    total_card = set(re.findall(r"\b\w+\b", total_card.lower())) - STOPWORDS
    question = set(re.findall(r"\b\w+\b", question.lower())) - STOPWORDS
    answer = set(re.findall(r"\b\w+\b", answer.lower())) - STOPWORDS

    num = len(total_card.intersection(question))
    den = len(total_card.intersection(answer))

    if den == 0: 
        return 0.0

    return num / den

def coverage_score_F1(total_card: str, question: str, answer : str) -> dict:
    total_card = set(re.findall(r"\b\w+\b", total_card.lower())) - STOPWORDS
    question = set(re.findall(r"\b\w+\b", question.lower())) - STOPWORDS
    answer = set(re.findall(r"\b\w+\b", answer.lower())) - STOPWORDS

    num = total_card.intersection(question)
    den = total_card.intersection(answer)

    all_symbols = num & den
    num = [1 if n in num else 0 for n in all_symbols]
    den = [1 if n in den else 0 for n in all_symbols]
    return sklearn.metrics.f1_score(num, den)


def coverage_score_per_token(total_card: str, question: str, answer : str) -> dict:
    score = coverage_score(total_card, question, answer)
    den = len(re.findall(r"\b\w+\b", answer.lower()))
    if den == 0: 
        return 0.0

    return score / den

# ---------------------------------------------------------------------------
# 2. HALLUCINATION RATE
# ---------------------------------------------------------------------------

# TODO: This has to be made better
def is_claim_supported(claim: str, source_text: str, threshold: float = 0.3) -> bool:
    claim_words  = set(re.findall(r"\b\w+\b", claim.lower())) - STOPWORDS
    source_words = set(re.findall(r"\b\w+\b", source_text.lower()))

    if not claim_words:
        return True
    overlap = claim_words & source_words
    return (len(overlap) / len(claim_words)) >= threshold


def hallucination_rate(description: str, source_text: str, threshold: float = 0.3) -> dict:
    """Estimate what fraction of the model's claims are NOT supported by the source."""
    
    sentences = description.split(". ") #= re.split(r"(?<=[.])\s+", text.strip())
    claims = [s.strip() for s in sentences if len(s.strip()) > 10]

    unsupported = [c for c in claims if not is_claim_supported(c, source_text, threshold)]
    return {
        "rate": len(unsupported) / len(claims) if claims else 0.0,
        "unsupported_claims": unsupported,
        "total_claims": len(claims),
    }

import ollama

def llm_as_judge(question: str, answer: str, gt: str, model="llama3.2:3b") -> float:
    try:
        response = ollama.generate(model=model, prompt=prompt)
        # Extract the first float found in the response
        score_str = response['response'].strip()
        return float(score_str)
    except Exception as e:
        try: 
            r = float(response['response'].strip().split("\n")[0])
            return r
        except: 
            print(f"Error during LLM judging: {e}, {response['response'].strip()}")            
        return 0.0