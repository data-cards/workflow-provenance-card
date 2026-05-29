import os, sys, re, math, json
from pathlib import Path
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# ── dependencies ────────────────────────────────────────────────────────────
try:
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAVE_ML = True
except ImportError:
    HAVE_ML = False
    print("[error] This script requires numpy, pandas, matplotlib, and seaborn.")

# ── paths ────────────────────────────────────────────────────────────────────
PATH_CARDS   = Path("ProvenanceCards/dataset/cards")
OUTPUT_DIR   = Path("ProvenanceCards/analysis_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────────────────

def load_cards(usecase: int) -> dict[str, str]:
    """Return {short_name: text} for all cards matching usecase."""
    cards: dict[str, str] = {}
    if not PATH_CARDS.exists(): return cards

    for fname in sorted(os.listdir(PATH_CARDS)):
        fpath = PATH_CARDS / fname
        if fpath.is_file() and str(usecase) in fname:
            cards[fname] = fpath.read_text(encoding="utf-8", errors="replace")

    wf = PATH_CARDS / f"workflow_cards/template_v4/{usecase}_workflow.md"
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

def lexical_diversity(tokens: list[str]) -> float:
    """Ratio of unique tokens to total tokens."""
    return len(set(tokens)) / len(tokens) if tokens else 0.0

def unigram_dist(tokens: list[str]) -> dict[str, float]:
    """Normalised unigram probability distribution."""
    c = Counter(tokens)
    total = sum(c.values()) or 1
    return {w: n / total for w, n in c.items()}

# ── plotting ──────────────────────────────────────────────────────────────────

def _plot_metric_stats(data_bins: dict, title: str, ylabel: str, filename: str):
    """Generic plotter for Mean + Std Dev per card type."""
    categories = list(data_bins.keys())
    means = [np.mean(data_bins[cat]) if data_bins[cat] else 0 for cat in categories]
    stds  = [np.std(data_bins[cat]) if data_bins[cat] else 0 for cat in categories]

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    # Use a distinct color palette
    colors = sns.color_palette("viridis", len(categories))
    bars = plt.bar(categories, means, yerr=stds, capsize=10, color=colors, edgecolor='black', alpha=0.8)
    
    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    plt.ylabel(ylabel, fontsize=12)
    plt.xlabel("Card Type", fontsize=12)
    plt.xticks(rotation=15)

    # Add numeric labels on top
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + (max(means)*0.02), 
                 f'{yval:.3f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=300)
    plt.close()

# ── main analysis ─────────────────────────────────────────────────────────────

def run():
    if not HAVE_ML: return

    # Mapping to group variations of filenames into clean categories
    category_map = {
        "data": "Data Card",
        "finetune": "Finetuned Card",
        "pretrain": "Pretrain Card",
        "workflow": "Workflow Card"
    }
    
    # Storage for the two metrics
    entropy_bins = {cat: [] for cat in category_map.values()}
    lex_div_bins = {cat: [] for cat in category_map.values()}

    # Aggregate data across all 5 usecases
    for uc in range(1, 6):
        cards = load_cards(uc)
        if not cards: continue

        for nm, txt in cards.items():
            tokens = tokenize(txt)
            if not tokens: continue
            
            # 1. Calculate Metrics
            dist = unigram_dist(tokens)
            ent = -sum(p * math.log2(p) for p in dist.values())
            ldiv = lexical_diversity(tokens)

            # 2. Categorize and Store
            lower_nm = nm.lower()
            for key, label in category_map.items():
                if key in lower_nm:
                    entropy_bins[label].append(ent)
                    lex_div_bins[label].append(ldiv)
                    break

    # ── Generation of Plots ──────────────────────────────────────────────────
    
    print("\nGenerating statistical plots...")

    # Plot 1: Entropy (Information Density)
    _plot_metric_stats(
        entropy_bins, 
        "Information Entropy (Mean & Std Dev)", 
        "Entropy (Bits)", 
        "stats_entropy.png"
    )
    print("  ✓ Saved: analysis_output/stats_entropy.png")

    # Plot 2: Lexical Diversity (Vocabulary Richness)
    _plot_metric_stats(
        lex_div_bins, 
        "Lexical Diversity (Mean & Std Dev)", 
        "Unique / Total Tokens Ratio", 
        "stats_lexical_diversity.png"
    )
    print("  ✓ Saved: analysis_output/stats_lexical_diversity.png")

if __name__ == "__main__":
    run()