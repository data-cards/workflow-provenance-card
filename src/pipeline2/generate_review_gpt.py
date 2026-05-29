import os
import pandas as pd
import requests
from pathlib import Path
from tqdm import tqdm

# --- Configuration ---
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "nemotron-3-nano"  # or "gpt-oss-120b" if you have it loaded in Ollama

# Paths
OUTPUTS_DIR = Path(".")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Define the specific card you want to query
SINGLE_CARD_PATH = Path("pipeline2_output/provenancecards/concat.md") 
QUESTIONS_PATH = "dataset/questions/questions_bench_2.csv"

# Load questions
QUESTIONS = pd.read_csv(QUESTIONS_PATH)["Question"]
ANSWERS = pd.read_csv("dataset/answers/template_v6/bench2/fromcard/nemotron-3-nano.csv")
answers = ANSWERS["Answer"].tolist()

def ollama_chat(prompt: str) -> str:
    """Sends a request to the local Ollama API."""
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "stream": False, # Set to False to get a single JSON response
        "options": {
            "temperature": 0.0,
            "top_p": 1.0
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=data)
        response.raise_for_status()
        result = response.json()
        return result['message']['content']
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        return None

import re
def try_parse_string_for_rating(s):
    match = re.search(r'\d+(?:\.\d+)?', s)
    if match:
        try:
            value = float(match.group())
            if 0.0 <= value <= 1.0:
                return value
        except ValueError:
            pass
    return None

def process_single_card(card_path: Path):
    if not card_path.exists():
        print(f"Error: Card file not found at {card_path}")
        return

    # Read the card content
    with open(card_path, "r") as f:
        card_content = f.read()

    # Construct the prompt
    card_prompt = (
        f"Context Card:\n{card_content}\n\n"
        "Task: Evaluate if the provided Answer correctly addresses the Question based strictly on the Context Card.\n"
        "Rules:\n"
        "1. Output exactly one numeric value between 0.0 (completely incorrect/unsupported) and 1.0 (completely correct).\n"
        "2. Output nothing else. No text, no markdown block, no explanation.\n"
    )

    ratings = []
    for q, a in tqdm(zip(QUESTIONS, answers)): 
        tprompt = card_prompt + f"\nQuestion: {q}\nAnswer: {a}\nRating:"
        # Query Ollama
        response = ollama_chat(tprompt)
        rate = try_parse_string_for_rating(response)
        ratings.append(rate if rate is not None else 0.0)

    if MODEL_NAME == "nemotron-3-nano":
        ANSWERS["Rating_N"] = ratings
    else: 
        ANSWERS["Rating_G"] = ratings
    ANSWERS.to_csv(f"dataset/answers/template_v6/bench2/fromcard/nemotron-3-nano.csv")

    # with open(out_filepath, "a") as f: 
    #     for r in ratings: 
    #         f.write(str(r) + "\n")
    # print(f"Results saved to: {out_filepath}")

if __name__ == "__main__":
    process_single_card(SINGLE_CARD_PATH)
    print("\nTask complete.")