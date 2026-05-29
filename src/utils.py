import math
import re
from collections import Counter
import os
from pathlib import Path

PATH_CARDS = Path("dataset/cards")

def load_cards(usecase: int, version=6) -> dict[str, str]:
    """Return {short_name: text} for all cards matching usecase."""
    cards: dict[str, str] = {}
    if not PATH_CARDS.exists(): return cards

    for fname in sorted(os.listdir(PATH_CARDS)):
        fpath = PATH_CARDS / fname
        if fpath.is_file() and str(usecase) in fname:
            cards[fname] = fpath.read_text(encoding="utf-8", errors="replace")

    wf = PATH_CARDS / f"workflow_cards/template_v{version}/{usecase}_workflow.md"
    if wf.exists():
        cards[wf.name] = wf.read_text(encoding="utf-8", errors="replace")
    return cards

def tokenize(text: str) -> list[str]:
    """Lowercase alpha tokens, length ≥ 2, no stopwords."""
    STOPWORDS = {
        "the","a","an","and","or","but","in","on","at","to","for","of","with",
        "is","are","was","were","be","been","being","have","has","had","do",
        "does","did","will","would","could","should","may","might","this","that",
        "these","those","it","its","as","by","from","into","not","no","so","if",
        "then","than","also","each","all","any","can","i","we","you","they","he",
        "she","which","who","what","when","where","how","about","more","other",
    }
    tokens = re.findall(r"[a-z]{2,}", text.lower())
    return [t for t in tokens if t not in STOPWORDS]


def unigram_dist(tokens: list[str]) -> dict[str, float]:
    """Normalised unigram probability distribution."""
    c = Counter(tokens)
    total = sum(c.values()) or 1
    return {w: n / total for w, n in c.items()}


def cross_entropy(p: dict[str, float], q: dict[str, float], smoothing: float = 1e-10) -> float:
    """H(p, q) = -Σ p(x) log q(x)  (nats).  Laplace-smoothed q."""
    vocab = set(p) | set(q)
    q_smooth = {w: q.get(w, 0) + smoothing for w in vocab}
    norm = sum(q_smooth.values())
    q_smooth = {w: v / norm for w, v in q_smooth.items()}
    return -sum(p.get(w, 0) * math.log(q_smooth[w]) for w in vocab if p.get(w, 0) > 0)


def kl_divergence(p: dict[str, float], q: dict[str, float], smoothing: float = 1e-10) -> float:
    """KL(p || q) = Σ p(x) log(p(x)/q(x))."""
    vocab = set(p) | set(q)
    q_smooth = {w: q.get(w, 0) + smoothing for w in vocab}
    norm = sum(q_smooth.values())
    q_smooth = {w: v / norm for w, v in q_smooth.items()}
    return sum(
        p.get(w, 0) * math.log((p.get(w, 0) + smoothing) / q_smooth[w])
        for w in vocab if p.get(w, 0) > 0
    )


def jaccard(set_a: set, set_b: set) -> float:
    if not set_a and not set_b:
        return 1.0
    return len(set_a & set_b) / len(set_a | set_b)


def lexical_diversity(tokens: list[str]) -> float:
    return len(set(tokens)) / len(tokens) if tokens else 0.0


def avg_sentence_len(text: str) -> float:
    sentences = re.split(r"[.!?]+", text)
    lens = [len(s.split()) for s in sentences if s.strip()]
    return sum(lens) / len(lens) if lens else 0.0


def heading_count(text: str) -> int:
    return len(re.findall(r"^#{1,6}\s", text, re.MULTILINE))


def code_block_count(text: str) -> int:
    return len(re.findall(r"```", text)) // 2

