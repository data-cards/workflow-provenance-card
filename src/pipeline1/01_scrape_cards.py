import os
import json
from huggingface_hub import ModelCard, DatasetCard

def save_card(repo_id, repo_type, base_path="dataset/cards"):
    """Downloads and saves a README.md (card) and returns the ID."""
    safe_name = repo_id.replace("/", "_")
    folder = os.path.join(base_path, repo_type, safe_name)
    os.makedirs(folder, exist_ok=True)
    
    file_path = os.path.join(folder, "README.md")
    
    try:
        if repo_type == "model":
            card = ModelCard.load(repo_id)
        else:
            card = DatasetCard.load(repo_id)
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(card.content)
        return card
    except Exception:
        return None

def scrape_and_map(finetuned_model_ids):
    lineage_map = []

    for ft_id in finetuned_model_ids:
        print(f"Mapping: {ft_id}...")
        ft_card = save_card(ft_id, "model")
        
        entry = {
            "finetuned_model": ft_id,
            "base_models": [],
            "datasets": []
        }

        if ft_card and hasattr(ft_card, 'data'):
            # Extract Base Model(s)
            base_model = ft_card.data.get("base_model")
            if ft_id == "tiiuae/falcon-7b-instruct": 
                base_model = "tiiuae/falcon-7b"
            elif ft_id in [ "ibm-nasa-geospatial/Prithvi-100M-multi-temporal-crop-classification","ibm-nasa-geospatial/Prithvi-100M-sen1floods11"]: 
                base_model = "ibm-nasa-geospatial/Prithvi-EO-1.0-100M"
            if base_model:
                bases = [base_model] if isinstance(base_model, str) else base_model
                for b_id in bases:
                    if save_card(b_id, "model"):
                        entry["base_models"].append(b_id)
            
            # Extract Dataset(s)
            datasets = ft_card.data.get("datasets")
            if datasets:
                ds_list = [datasets] if isinstance(datasets, str) else datasets
                for ds_id in ds_list:
                    if save_card(ds_id, "dataset"):
                        entry["datasets"].append(ds_id)
        
        lineage_map.append(entry)

    # Save the mapping to JSON
    with open("dataset/model_lineage.json", "w", encoding="utf-8") as jf:
        json.dump(lineage_map, jf, indent=4)
    
    print("\nLineage mapping saved to 'model_lineage.json'")

if __name__ == "__main__":
    target_models = [
        # LLMs
        "prithivMLmods/Llama-Doctor-3.2-3B-Instruct", 
        # "tiiuae/falcon-7b-instruct",
        # "HuggingFaceH4/zephyr-7b-beta",
        # "CreitinGameplays/ConvAI-9b-v2",

        # reasoning
        "empero-ai/openNemo-Cascade-2-30B-A3B",

        # Earth Observation & Geospatial (IBM/NASA Prithvi)
        "ibm-nasa-geospatial/Prithvi-100M-multi-temporal-crop-classification",
            
        # Security
        "cybersectony/phishing-email-detection-distilbert_v2.4.1",
        # "CrabInHoney/urlbert-tiny-v4-phishing-classifier",
        
        # Coding & Software Engineering
        "chinu-codes/llama-3.2-3b-pii-redactor-lora",
    ]
    
    scrape_and_map(target_models)

    # Workflow prepared are: 
    # - Llama-Doctor-3.2-3B-Instruct finetuning from Llama-3.2-3B
    # - openNemo-Cascade-2-30B-A3B finetuning
    # - Prithvi-100M-multi-temporal-crop-classification finetuning from Prithvi-100M
    # - phishing-email-detection-distilbert_v2.4.1 finetuning from distilbert
    # - llama-3.2-3b-pii-redactor-lora finetuning from Llama-3.2-3B


# 