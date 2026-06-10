
from pathlib import Path
import os

path = Path("dataset/cards/")
concat = Path("dataset/concat/")
os.system(f"rm -rf {concat}")
os.makedirs(concat, exist_ok=True)

files = sorted(path.glob("*.md")) + sorted((path / "workflow_cards").glob("*.md"))

for I in range(1, 6): 
    relevant_workflow = [file for file in files if file.name.split("_")[0] == str(I)]

    for remove in range(len(relevant_workflow)): 
        final_card = []
        for current, file in enumerate(relevant_workflow): 
            if current == remove: 
                continue
            else: 
                final_card.append(file)
    
        with open(concat / f"{I}_concat_without_{remove}.md", "w") as f: 
            f.write("\n".join([open(f).read() for f in final_card]))

for I in range(1, 6): 
    relevant_workflow = [file for file in files if file.name.split("_")[0] == str(I)]

    final_card = []
    for current, file in enumerate(relevant_workflow): 
        final_card.append(file)

    with open(concat / f"{I}_concat.md", "w") as f: 
        f.write("\n".join([open(f).read() for f in final_card]))
