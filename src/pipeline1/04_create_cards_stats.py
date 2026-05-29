import os, sys, re, math
from pathlib import Path
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# ── dependencies ────────────────────────────────────────────────────────────
try:
    import numpy as np
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAVE_ML = True
except ImportError:
    HAVE_ML = False
    # print("[warn] scikit-learn / matplotlib not found – falling back to pure-Python stats.")

# ── paths ────────────────────────────────────────────────────────────────────
PATH_CARDS   = Path("ProvenanceCards/dataset/cards")
OUTPUT_DIR   = Path("ProvenanceCards/analysis_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────────────────

def load_cards(usecase: int) -> dict[str, str]:
    """Return {short_name: text} for all cards matching usecase."""
    cards: dict[str, str] = {}

    # regular cards
    for fname in sorted(os.listdir(PATH_CARDS)):
        fpath = PATH_CARDS / fname
        if fpath.is_file() and str(usecase) in fname:
            text = fpath.read_text(encoding="utf-8", errors="replace")
            cards[fname] = text

    # workflow card
    wf = PATH_CARDS / f"workflow_cards/template_v4/{usecase}_workflow.md"
    if wf.exists():
        cards[wf.name] = wf.read_text(encoding="utf-8", errors="replace")
    else:
        print(f"[warn] workflow card not found: {wf}")

    # print(cards)
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


# ── main analysis ─────────────────────────────────────────────────────────────

def run(usecase: int = 1):
    df_ces = []
    df_jacs = []
    for usecase in range(1, 6): 
        cards = load_cards(usecase)
        if not cards:
            print(f"[error] No cards found for usecase={usecase} in {PATH_CARDS}")
            sys.exit(1)

        names  = list(cards.keys())
        texts  = list(cards.values())
        short  = [n[:35] for n in names]   # truncate for display
        n      = len(names)

        # print(f"\n{'═'*60}")
        # print(f"  Cards loaded: {n}  |  usecase={usecase}")
        # print(f"{'═'*60}")
        # for nm in names:
            # print(f"  • {nm}")

        # ── token data ──────────────────────────────────────────────────────────
        token_lists = [tokenize(t) for t in texts]
        dists       = [unigram_dist(tl) for tl in token_lists]
        token_sets  = [set(tl) for tl in token_lists]

        # ── per-card stats ───────────────────────────────────────────────────────
        per_card = []
        for i, (nm, txt, tl) in enumerate(zip(names, texts, token_lists)):
            per_card.append({
                "card":              nm,
                "char_count":        len(txt),
                "word_count":        len(txt.split()),
                "unique_tokens":     len(set(tl)),
                "total_tokens":      len(tl),
                "lexical_diversity": round(lexical_diversity(tl), 4),
                "avg_sentence_len":  round(avg_sentence_len(txt), 1),
                "heading_count":     heading_count(txt),
                "code_blocks":       code_block_count(txt),
                "entropy_bits":      round(-sum(p * math.log2(p) for p in dists[i].values()), 3),
            })

        df_per = pd.DataFrame(per_card) if HAVE_ML else per_card
        # print("\n── Per-card statistics ──────────────────────────────────────")
        if HAVE_ML:
            pd.set_option("display.max_columns", None)
            pd.set_option("display.width", 120)
            # print(df_per.to_string(index=False))
        # else:
            # for row in per_card:
                # print(row)

        # ── pairwise matrices ────────────────────────────────────────────────────
        ce_matrix  = [[0.0]*n for _ in range(n)]
        kl_matrix  = [[0.0]*n for _ in range(n)]
        jac_matrix = [[0.0]*n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                ce_matrix[i][j]  = round(cross_entropy(dists[i], dists[j]), 4)
                kl_matrix[i][j]  = round(kl_divergence(dists[i], dists[j]), 4)
                jac_matrix[i][j] = round(jaccard(token_sets[i], token_sets[j]), 4)

        if HAVE_ML:
            df_ce  = pd.DataFrame(ce_matrix,  index=short, columns=short)
            df_kl  = pd.DataFrame(kl_matrix,  index=short, columns=short)
            df_jac = pd.DataFrame(jac_matrix, index=short, columns=short)

            # TF-IDF cosine similarity
            tfidf = TfidfVectorizer(tokenizer=tokenize, token_pattern=None)
            tfidf_mat = tfidf.fit_transform(texts)
            cos_sim   = cosine_similarity(tfidf_mat)
            df_cos    = pd.DataFrame(cos_sim, index=short, columns=short).round(4)

            # print("\n── Cross-entropy matrix H(row, col) ─────────────────────────")
            # print(df_ce.to_string())

            # print("\n── KL divergence KL(row || col) ─────────────────────────────")
            # print(df_kl.to_string())

            # print("\n── Jaccard vocabulary overlap ───────────────────────────────")
            # print(df_jac.to_string())

            # print("\n── TF-IDF cosine similarity ─────────────────────────────────")
            # print(df_cos.to_string())

            # save CSVs
            df_ce.to_csv(OUTPUT_DIR / "cross_entropy_matrix.csv")
            df_kl.to_csv(OUTPUT_DIR / "kl_divergence_matrix.csv")
            df_jac.to_csv(OUTPUT_DIR / "jaccard_similarity_matrix.csv")
            df_cos.to_csv(OUTPUT_DIR / "cosine_similarity_matrix.csv")
            pd.DataFrame(per_card).to_csv(OUTPUT_DIR / "per_card_stats.csv", index=False)

            # ── shared top-N concepts ────────────────────────────────────────────
            top_k   = 20
            top_per = [Counter(tl).most_common(top_k) for tl in token_lists]
            all_top = set()
            for lst in top_per:
                all_top.update(w for w, _ in lst)

            concept_rows = []
            for word in sorted(all_top):
                row = {"concept": word}
                for nm, tl in zip(names, token_lists):
                    row[nm[:20]] = Counter(tl).get(word, 0)
                concept_rows.append(row)
            df_concepts = pd.DataFrame(concept_rows).sort_values(
                by=[c for c in concept_rows[0] if c != "concept"], ascending=False
            )
            df_concepts.to_csv(OUTPUT_DIR / "shared_concepts.csv", index=False)

            # ── redundancy alerts ────────────────────────────────────────────────
            # print("\n── Redundancy alerts (Jaccard > 0.3, excluding diagonal) ────")
            found = False
            for i in range(n):
                for j in range(i+1, n):
                    if jac_matrix[i][j] > 0.3:
                        # print(f"  ⚠  {short[i]}  ↔  {short[j]}  Jaccard={jac_matrix[i][j]:.3f}")
                        found = True
            if not found:
                print("  ✓  No high-overlap pairs found at Jaccard > 0.3")

            # ── workflow coverage gap ────────────────────────────────────────────
            wf_name = next((nm for nm in names if "workflow" in nm.lower()), None)
            if wf_name:
                wf_idx   = names.index(wf_name)
                wf_top   = {w for w, _ in Counter(token_lists[wf_idx]).most_common(50)}
                other_tokens = set()
                for i, nm in enumerate(names):
                    if i != wf_idx:
                        other_tokens |= token_sets[i]
                gap = wf_top - other_tokens
                # print(f"\n── Workflow terms missing from regular cards ────────────────")
                # print(f"  {sorted(gap) or '(none – full coverage)'}")

        df_ces.append(np.expand_dims(df_ce.values, axis=0))
        df_jacs.append(np.expand_dims(df_jac.values, axis=0))

    df_ces = np.concatenate(df_ces, axis=0)
    df_jacs = np.concatenate(df_jacs, axis=0)

    mean_ce = df_ces.mean(axis=0)
    std_ce = df_ces.std(axis=0)
    mean_jac = df_jacs.mean(axis=0)
    std_jac = df_jacs.std(axis=0)

    _heatmap_html(mean_ce, f"Mean over all UCs for Cross-entropy", "rocket_r")
    _heatmap_html(std_ce, f"Std. Dev. over all UCs for Cross-entropy", "rocket_r")
    _heatmap_html(mean_jac, f"Mean over all UCs for Vocab Overlap", "Greens")
    _heatmap_html(std_jac, f"Std. Dev. over all UCs for Vocab Overlap", "Greens")

    # _heatmap_html(df_cos, "TF-IDF Cosine Similarity", "Blues")

# ── HTML report writer ────────────────────────────────────────────────────────

def _heatmap_html(df: "pd.DataFrame", title: str, cmap: str = "YlOrRd") -> str:
    fig, ax = plt.subplots(figsize=(max(6, len(df)*1.1), max(5, len(df)*0.9)))
    sns.heatmap(df.astype(float), annot=True, fmt=".3f", cmap=cmap, linewidths=0.5, ax=ax, cbar=True)
    ax.set_title(title, fontsize=13, pad=12)
    plt.xticks([i + 0.5 for i in range(4)], ["Data Card", "Finetuned Model Card", "Pretrain Model Card", "Workflow Card"], rotation=45)
    plt.yticks([i + 0.5 for i in range(4)], ["Data Card", "Finetuned Model Card", "Pretrain Model Card", "Workflow Card"], rotation=0)
    plt.tight_layout()
    path = OUTPUT_DIR / f"_tmp_{title.replace(' ','_')}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    usecase = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    run(usecase)