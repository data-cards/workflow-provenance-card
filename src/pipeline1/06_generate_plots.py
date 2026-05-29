import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── paths (edit if needed) ────────────────────────────────────────────────────
FILE1 = "results/leaveoneout2.csv"   # leave-one-out
FILE2 = "results/leaveoneout3.csv"   # baseline / single-card

OUTPUT_DIR = "./figures"             # where to save figures
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── palette ───────────────────────────────────────────────────────────────────
CARD_COLORS = {
    "DataCard":           "#4C72B0",
    "Finetuning Model Card": "#DD8452",
    "Pretraining Model Card":"#55A868",
    "Workflow Card":      "#C44E52",
}
DIFF_COLOR   = "#8172B3"
EASY_COLOR   = "#2ca02c"
MED_COLOR    = "#ff7f0e"
HARD_COLOR   = "#d62728"
DIFFICULTY_PALETTE = {"easy": EASY_COLOR, 
                    #   "medium": MED_COLOR, 
                      "hard": HARD_COLOR}

METRICS      = ["similarity", "llm_as_judge_1", "llm_as_judge_2"]
METRIC_LABELS = ["Similarity", "LLM Judge"]

# ── helpers ───────────────────────────────────────────────────────────────────
def composite(df: pd.DataFrame) -> pd.Series:
    return df[METRICS].mean(axis=1)

def llm_judge(df: pd.DataFrame) -> pd.Series:
    """Average of the two LLM-as-judge columns."""
    return df[["llm_as_judge_1", "llm_as_judge_2"]].mean(axis=1)

def savefig(name: str):
    path = os.path.join(OUTPUT_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  saved → {path}")

# ═════════════════════════════════════════════════════════════════════════════
# 1. LOAD & PREPARE
# ═════════════════════════════════════════════════════════════════════════════
print("Loading data …")
df1 = pd.read_csv(FILE1, sep=";")
df2 = pd.read_csv(FILE2, sep=";")

# map numeric 'without' codes → card names
card_map = {
    0: "Without\nDataCard",
    1: "Without Finetuning\nModel Card",
    2: "Without Pretraining\nModel Card",
    3: "Without\nWorkflow Card",
}
df1["card_removed"] = df1["without"].map(card_map)

# composite score
df1["composite"] = composite(df1)
df2["composite"] = composite(df2)

# difficulty order
diff_order = ["easy", "hard"]

print(f"  File 1: {len(df1)} rows  |  cards removed: {sorted(df1['card_removed'].unique())}")
print(f"  File 2: {len(df2)} rows  |  modalities: {sorted(df2['without'].unique())}")
print()


# ═════════════════════════════════════════════════════════════════════════════
# 2.  FIGURE 1 — Leave-one-out: LLM-judge score per card removed + reference
# ═════════════════════════════════════════════════════════════════════════════
print("Figure 1: per-card LLM-judge scores with reference …")

card_order = list(card_map.values())

# LLM-judge score for each leave-one-out condition
df1["llm_judge"] = llm_judge(df1)
loo_means = (
    df1.groupby("card_removed")["llm_judge"]
    .mean()
    .reindex(card_order)
)

# Reference = "all cards present" (concat row from FILE2)
df2["llm_judge"] = llm_judge(df2)
reference_score = df2.loc[df2["without"] == "concat", "llm_judge"].mean()

fig, ax = plt.subplots(figsize=(8, 5))
colors = list(CARD_COLORS.values())
x = np.arange(len(card_order))
bar_width = 0.55

bars = ax.bar(x, loo_means.values, width=bar_width, color=colors, alpha=0.88, zorder=3)

# Annotate bars
for bar, val in zip(bars, loo_means.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        val + 0.008,
        f"{val:.3f}",
        ha="center", va="bottom", fontsize=10, fontweight="bold"
    )

# Reference line
ax.axhline(reference_score, color="#333333", linewidth=1.8, linestyle="--", zorder=4,
           label=f"Reference – all cards ({reference_score:.3f})")

ax.text(
    0.05, 0.95, 'optimum $\\uparrow$',
    transform=ax.transAxes, ha='left', va='top', color='grey', fontsize=11,
)

ax.set_xticks(x)
ax.set_xticklabels(card_order, fontsize=11)
ax.set_ylabel("Mean LLM-as-Judge Score", fontsize=12)
ax.set_title("LLM-Judge Score When Each Card Is Removed (Leave-One-Out)", fontsize=13, fontweight="bold")
ax.set_ylim(0, 0.8)
ax.legend(fontsize=10, loc="upper right")
ax.grid(axis="y", alpha=0.3, zorder=0)
fig.tight_layout()
savefig("fig1_card_mean_scores.pdf")

# ═════════════════════════════════════════════════════════════════════════════
# 3.  FIGURE 2 — Single-card context: absolute LLM-judge scores + reference
# ═════════════════════════════════════════════════════════════════════════════

print("Figure 2: single-card absolute LLM-judge scores with reference …")

modality_rename = {
    "concat":      "All Cards\n(Reference)",
    "datacard":    "DataCard\nOnly",
    "finetuned":   "Finetuning MC\nOnly",
    "pretrained":  "Pretraining MC\nOnly",
    "workflow":    "Workflow Card\nOnly",
    "workflowcard":"Workflow Card\nOnly",
}
df2["modality"] = df2["without"].map(modality_rename)

summary2 = df2.groupby("modality")["llm_judge"].mean()

# Separate reference from single-card conditions
ref_label  = "All Cards\n(Reference)"
ref_score  = summary2.loc[ref_label]

mod_order = [
    "DataCard\nOnly",
    "Finetuning MC\nOnly",
    "Pretraining MC\nOnly",
    "Workflow Card\nOnly",
]
scores = summary2.reindex(mod_order)

bar_colors = [
    CARD_COLORS["DataCard"],
    CARD_COLORS["Finetuning Model Card"],
    CARD_COLORS["Pretraining Model Card"],
    CARD_COLORS["Workflow Card"],
]

fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(mod_order))

bars = ax.bar(x, scores.values, color=bar_colors, alpha=0.88, zorder=3, width=0.55)

# Annotate bars
for bar, val in zip(bars, scores.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        val + 0.007,
        f"{val:.3f}",
        ha="center", va="bottom", fontsize=10, fontweight="bold"
    )

# Reference line
ax.axhline(ref_score, color="#333333", linewidth=1.8, linestyle="--", zorder=4,
           label=f"Reference – all cards ({ref_score:.3f})")

ax.text(
    0.05, 0.95, 'optimum $\\uparrow$',
    transform=ax.transAxes, ha='left', va='top', color='grey', fontsize=11,
)

ax.set_xticks(x)
ax.set_xticklabels(mod_order, fontsize=10)
ax.set_ylabel("Mean LLM-as-Judge Score", fontsize=12)
ax.set_title("LLM-Judge Score vs. Full Reference (Single-Card)",
             fontsize=13, fontweight="bold")
ax.set_ylim(0, 0.8)
ax.legend(fontsize=10, loc="upper right")
ax.grid(axis="y", alpha=0.3, zorder=0)
fig.tight_layout()
savefig("fig2_single_card_degradation.pdf")

# ═════════════════════════════════════════════════════════════════════════════
# 4.  FIGURE 3 — Difficulty vs. score (file 1 leave-one-out)
# ═════════════════════════════════════════════════════════════════════════════
print("Figure 3: difficulty vs composite score …")

diff_means = (
    df1.groupby(["type_", "card_removed"])["composite"]
    .mean()
    .unstack("card_removed")
    .reindex(diff_order)
    [card_order]
)

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(diff_order))
width = 0.2
diff_means.T.plot.bar(color=list(CARD_COLORS.values()), ax=ax)
ax.set_xticklabels(list(card_map.values()), rotation=45)#["Easy", "Medium", "Hard"], fontsize=12)
ax.set_xlabel("Card Removed", fontsize=12)
ax.set_ylabel("Mean Composite Score", fontsize=12)
ax.set_title("Composite Score by Difficulty & Card Removed", fontsize=13, fontweight="bold")
ax.set_ylim(0, 1.0)
ax.legend(title="Card Removed", fontsize=9)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
savefig("fig3_difficulty_by_card.pdf")

# ═════════════════════════════════════════════════════════════════════════════
# 7. FIGURE 6 — One Card Only Validation (Heatmap)
# ═════════════════════════════════════════════════════════════════════════════
print("Figure 6: one card only validation heatmap …")

# Join and prepare the data
questions = pd.read_csv("dataset/questions/questions_bench_1.csv")
df2_joined = df2.join(questions, on="answer")

# Aggregate by 'without' (the card) and 'Type' (difficulty)
# We pivot so cards are columns and difficulty types are rows
df2_pivot = (
    df2_joined.groupby(["without", "Type"])["composite"]
    .mean()
    .reset_index()
    .pivot(index="Type", columns="without", values="composite")
)

# Ensure the difficulty order is consistent with previous charts
diff_order = ["easy", "hard"]
available_indices = [d for d in diff_order if d in df2_pivot.index]

# Plotting
fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(
    df2_pivot, 
    annot=True, 
    fmt=".2f", 
    cmap="RdYlGn", 
    cbar_kws={'label': 'Mean LLM-as-Judge Score'},
    ax=ax,
    annot_kws={"fontweight": "bold"}
)

# Styling to match previous figures
ax.set_title("Performance with only one card, split by question's focus", 
             fontsize=13, fontweight="bold", pad=20)
ax.set_xlabel("Card Used", fontsize=12)
ax.set_ylabel("Question Focus", fontsize=12)

# Clean up labels (Capitalize difficulties and clean card names)
ax.set_yticklabels([t.get_text().capitalize() for t in ax.get_yticklabels()], rotation=0)
ax.set_xticklabels(["Top\nAnswer", "Only\nData Card", "Only\nFinetuning MC", "Only\nPretraining MC", "Only\nWorkflow Card"])

fig.tight_layout()
savefig("fig6_one_card_validation_heatmap.pdf")

# ── FIGURE 6 TABLE GENERATION ────────────────────────────────────────────────
print("\n" + "="*80)
print("TABLE FOR FIGURE 6: VALUES IN RANGE [0, Top Answer]")
print("="*80)

# 1. Ensure the pivot is correctly formed
# We look at the actual values in the 'without' column to avoid key errors
available_modalities = df2_joined['without'].unique()

# Mapping for the columns (internal names -> display names)
col_map = {
    "baseline":    "Top Answer",
    "datacard":    "Only DataCard",
    "finetuned":   "Only Finetuning MC",
    "pretrained":  "Only Pretraining MC",
    "workflow":    "Only Workflow Card",
    "workflowcard":"Only Workflow Card" # Handle variant
}

# 2. Extract the pivoted data
# We use the 'Type' from questions as the index (Difficulty/Category)
table_raw = (
    df2_joined.groupby(["Type", "without"])["composite"]
    .mean()
    .unstack("without")
)

# 3. Handle Scaling: [0, Top Answer] 
# Absolute values are already in this range relative to the baseline.
# We will filter and rename to match your request.
cols_to_print = [c for c in col_map.keys() if c in table_raw.columns]
final_table = table_raw[cols_to_print].rename(columns=col_map)

# Remove duplicate 'Only Workflow Card' if both 'workflow' and 'workflowcard' exist
final_table = final_table.loc[:, ~final_table.columns.duplicated()]

print("--- Absolute Mean Scores ---")
print(final_table.round(4).to_string())

# 4. Normalized Table (Scaled so Top Answer = 1.0)
print("\n--- Normalized to Top Answer (Baseline = 1.0) ---")
if "baseline" in table_raw.columns:
    norm_table = table_raw[cols_to_print].div(table_raw["baseline"], axis=0).rename(columns=col_map)
    norm_table = norm_table.loc[:, ~norm_table.columns.duplicated()]
    print(norm_table.to_string())
else:
    print("Baseline column not found, could not normalize.")

print("="*80)

# ═════════════════════════════════════════════════════════════════════════════
# 8. FIGURE 8 — Data size of provenance cards
# ═════════════════════════════════════════════════════════════════════════════
print("Figure 8: size of cards related to use case and card type …")

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

path = Path("dataset/cards")
all_files = [f for f in os.listdir(path) if f.endswith('.md')] + [ "workflow_cards/template_v6/" +f for f in os.listdir("dataset/cards/workflow_cards/template_v6") if f.endswith('.md')] # Assuming json cards

# Helper function to convert bytes to KB
def to_kb(size_list):
    return [s / 1024 for s in size_list]

# --- Data Preparation for Subplot 1 (Card Type) ---
card_types = ["workflow", "data", "model"]
type_sizes = {t: to_kb([os.path.getsize(path / f) for f in all_files if t in f]) for t in card_types}
type_means = [np.mean(type_sizes[t]) if type_sizes[t] else 0 for t in card_types]

# --- Data Preparation for Subplot 2 (Use Case x Card Type) ---
use_cases = ["1", "2", "3", "4", "5"]
# We'll create a matrix: rows = use cases, columns = card types
grouped_data = []
for uc in use_cases:
    row = []
    for t in card_types:
        sizes = to_kb([os.path.getsize(path / f) for f in all_files if uc in f and t in f])
        row.append(np.mean(sizes) if sizes else 0)
    grouped_data.append(row)
grouped_data = np.array(grouped_data) # Shape: (5, 3)
print(grouped_data)

# --- Plotting ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
colors = ["#66c2a5", "#fc8d62", "#8da0cb"] # Consistent with previous diff colors

# Subplot 1: Mean Size by Card Type
ax1.bar(card_types, type_means, color=colors, edgecolor='black', alpha=0.8)
ax1.set_title("Mean Card Size by Type", fontsize=13, fontweight="bold")
ax1.set_ylabel("Size (KB)", fontsize=12)
ax1.grid(axis='y', linestyle='--', alpha=0.6)
ax1.set_xticklabels([t.capitalize() for t in card_types])

# Subplot 2: Grouped Bar Chart (Use Case and Card Type)
x = np.arange(len(use_cases))
width = 0.25

for i, t in enumerate(card_types):
    ax2.bar(x + (i * width), grouped_data[:, i], width, label=t.capitalize(), 
            color=colors[i], edgecolor='black', alpha=0.8)

ax2.set_title("Mean Size by Use Case & Card Type", fontsize=13, fontweight="bold")
ax2.set_xlabel("Use Case ID", fontsize=12)
ax2.set_xticks(x + width)
ax2.set_xticklabels([f"UC {uc}" for uc in use_cases])
ax2.legend(title="Card Type")
ax2.grid(axis='y', linestyle='--', alpha=0.6)

fig.suptitle("Provenance Card Data Size Analysis", fontsize=15, fontweight="bold")
# fig.tight_layout(rect=[0, 0.03, 1, 0.95])

savefig("fig8_card_sizes.pdf")