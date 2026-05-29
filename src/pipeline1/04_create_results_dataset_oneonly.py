
import os
from pathlib import Path
import pandas as pd
from tqdm import tqdm
import sys
sys.path.append("./")
sys.path.append("./ProvenanceCards")
from src.metrics_pipeline import *

PATH_ANSWERS = Path("ProvenanceCards/dataset/answers/template_v6/")
PATH_CARDS = Path("ProvenanceCards/dataset/concat/")
PATH_QUESTIONS = Path("ProvenanceCards/dataset/questions/questions_bench_1.csv")

USECASES = [1, 2, 3, 4, 5]

def get_params_from_path(path): 
    path = path.split("/")[-1]
    usecase = path.split("_")[0]#int(path.split("_")[0])
    kind = path.split("_")[-1].replace(".md", "")
    return usecase, kind

def get_metrics_for_answer(path): 
    path = str(path)
    questions = pd.read_csv(PATH_QUESTIONS)
    usecase, kind = get_params_from_path(path)
    answers = pd.read_csv(path, sep="\t", header=None)
    if len(answers.columns) == 2: 
        answers.columns = ["question", "answer"]
    else: 
        answers.columns = ["question", "answer", "summary"]
    answers = answers.fillna("")

    gts = pd.read_csv(f"ProvenanceCards/dataset/gt/{usecase}_answers.csv", sep=";")

    # card_data = open(PATH_CARDS / f"{usecase}_concat_without_{without}.md", "r").read()

    results = []
    for i, _, cat, question, type_ in questions.itertuples(): 

        answer = str(answers.iloc[i]["answer"]).strip()
        gt = str(gts.iloc[i]["a"]).strip()
        question = str(question).strip()

        # c1 = coverage_score(card_data, question, answer)
        # c2 = coverage_score_F1(card_data, question, answer)
        # c3 = coverage_score_per_token(card_data, question, answer)
        # c4 = check_correctness(question, answer)
        c5 = check_gt_similarity(answer, gt)
        c6 = llm_as_judge(question, answer, gt, model="llama3.2:3b")
        c7 = llm_as_judge(question, answer, gt, model="phi4-mini")

        results.append({
            # "question": question_id, 
            "type_": type_, 
            "category": cat, 
            "answer": i, 
            "usecase": usecase, 
            "without": kind, 
            # "coverage_acc": c1, 
            # "coverage_F1": c2, 
            # "coverage_per_token": c3, 
            # "correctness": c4, 
            "similarity": c5, 
            "llm_as_judge_1": c6, 
            "llm_as_judge_2": c7, 
        })

    return results


if __name__ == "__main__":
    all_answers = [PATH_ANSWERS / f for f in os.listdir(PATH_ANSWERS) if "without" not in f and int(f.split("_")[0]) in USECASES]

    # final_results = []
    # for answer in tqdm(all_answers):
    #     results = get_metrics_for_answer(answer)
    #     # question_id = int(str(answer).split("/")[-1].replace(".md", "").split("_")[-1])

    #     final_results.extend(results)
    
    # data = pd.DataFrame(final_results)
    # data.to_csv("results/leaveoneout3.csv", sep=";")

    for i, answer in enumerate(tqdm(all_answers)):
        print(answer)
        if Path(f"{i}_boh.csv").exists(): 
            continue
        results = get_metrics_for_answer(answer)
        pd.Series(results).to_csv(f"{i}_boh.csv", sep=";")
    
    final_results = []
    for i, answer in enumerate(tqdm(all_answers)):
        d = pd.read_csv(f"{i}_boh.csv", sep=";", index_col=0)
        d = [eval(f) for f in d.iloc[:, 0].values.tolist()]
        final_results.extend(d)

    data = pd.DataFrame(final_results)
    data.to_csv("ProvenanceCards/results/leaveoneout3.csv", sep=";")