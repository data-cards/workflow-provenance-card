import os
import pandas as pd
import requests
from pathlib import Path

# --- Configuration ---
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "nemotron-3-nano"  # or "gpt-oss-120b"

# Paths
OUTPUTS_DIR = Path(".")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Define the specific card you want to query
SINGLE_CARD_PATH = Path("pipeline2_output/provenancecards/concat.md") 
QUESTIONS_PATH = "dataset/questions/questions_bench_2.csv"

# Load questions
QUESTIONS = pd.read_csv(QUESTIONS_PATH)["Question"]

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

def process_single_card(card_path: Path):
    if not card_path.exists():
        print(f"Error: Card file not found at {card_path}")
        return

    print(f"Processing card: {card_path.name}")
    # out_filepath = OUTPUTS_DIR / f"answer_{card_path.name}"

    # Read the card content
    with open(card_path, "r") as f:
        card_content = f.read()

    # Construct the prompt
    prompt = card_content
    prompt += (
        "\nBased strictly on the provided cards, without assuming or making up any facts outside of them:"
        "Answer each question in the absolute fewest words possible."
        "Output only the answers, separating each one with a single newline character (\n)."
        "Do not include headers, numbering, introductory phrases, or concluding text.\n"
        # "\nWith reference to these cards and only these cards, without making up information, "
        # "answer the following questions the least amount of words possible, and return string "
        # "containing in each row one of the answers, separated by the '\n' token, "
        # "and include no header and no initial phrase, I want to be able to parse all the answers simply "
        # "splitting on the new row token:\n"
        # TODO ask gpt --> judges agree ment on bench 2
    )
    prompt += "\n".join(QUESTIONS.tolist())

    # Query Ollama
    response = ollama_chat(prompt)

    answers = response.replace(",", ";").split("\n")

    ANSWERS = pd.read_csv(QUESTIONS_PATH)#pd.read_csv(f"ProvenanceCards/dataset/answers/template_v6/bench2/fromjsonl/{MODEL_NAME}.csv")
    ANSWERS["Answer"] = answers
    ANSWERS.to_csv(f"dataset/answers/template_v6/bench2/fromcard/{MODEL_NAME}.csv")

if __name__ == "__main__":
    process_single_card(SINGLE_CARD_PATH)
    print("\nTask complete.")