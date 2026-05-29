
import pandas as pd
from pathlib import Path

USECASE = 1
TYPE = "concat_without_0"
ANSWERS = Path(f"dataset/answers/template_v5/{USECASE}_{TYPE}.md") # question, answer
QUESTIONS = Path("dataset/questions/Questions_latest.csv") # question
GTS = Path(f"dataset/gt/{USECASE}_answers.csv") # "q";"a";"reasoning"
SCORES_LEAVEONEOUT = Path("results/leaveoneout2.csv") # type_;category;answer;usecase;without;similarity;llm_as_judge_1;llm_as_judge_2
SCORES_ONEONLY = Path("results/leaveoneout3.csv") # type_;category;answer;usecase;without;similarity;llm_as_judge_1;llm_as_judge_2

answers = pd.read_csv(ANSWERS, sep="\t", header=None)
answers.columns = ["question", "answer"]
questions = pd.read_csv(QUESTIONS)
gts = pd.read_csv(GTS, sep=";")
if "without" in TYPE: 
    scores = pd.read_csv(SCORES_LEAVEONEOUT, sep=";")
    without = int(TYPE.split("_")[-1])
else: 
    scores = pd.read_csv(SCORES_ONEONLY, sep=";")
filtered_scores = scores[
    (scores['usecase'] == USECASE) & 
    (scores['without'] == without)
].copy()

filtered_scores['question_text'] = filtered_scores['answer'].apply(lambda x: answers.iloc[x]['question'])
filtered_scores['answer_text'] = filtered_scores['answer'].apply(lambda x: answers.iloc[x]['answer'])

filtered_scores['gt_answer'] = filtered_scores['answer'].apply(lambda x: gts.iloc[x]['a'])
filtered_scores['gt_reasoning'] = filtered_scores['answer'].apply(lambda x: gts.iloc[x]['reasoning'])

result = filtered_scores.merge(
    questions, 
    left_on='answer', # or whichever column holds the Q index
    right_index=True, 
    how='inner'
)

filtered_scores.to_csv(f"{USECASE}_{TYPE}.csv", sep=";", columns=["llm_as_judge_1","llm_as_judge_2","answer_text","gt_answer","question_text","type_","category","answer","usecase","without","similarity","gt_reasoning"])