from flowcept.agents.flowcept_agent import FlowceptAgent
import json
import time
import pandas as pd

MODEL = "gpt-oss-120b"
datapath = "ProvenanceCards/pipeline2_output/jsons/flowcept_buffer.jsonl"

QUESTIONS = pd.read_csv("ProvenanceCards/dataset/questions/questions_bench_2.csv")["Question"].tolist()
agent = FlowceptAgent(buffer_path=datapath)
agent.start()
time.sleep(2)  # Give Uvicorn a second to bind to the port

indices = None#range(28, 32)#[3, 7, 8, 16, 19, 26, 28, 29, 30]

def try_parse_answer(s): 
    return s

answers = []
for i, q in enumerate(QUESTIONS): 
    if indices is not None and i not in indices: 
        continue
    
    resp = agent.query(f"Answer the following question in a short way, without making up information, and return all the results in a string, even if the question asks you to list, return a string. \n - {QUESTIONS[i]}")

    answer = None
    try: 
        answer = try_parse_answer(resp.result["result_df"])
    except: 
        pass
    if answer is None: 
        try: 
            answer = try_parse_answer(resp.result)
        except: 
            pass
    if answer is None: 
        try: 
            answer = try_parse_answer(resp.result["summary"])
        except: 
            pass
    answers.append(answer if answer is not None else "N/A")
agent.stop()

ANSWERS = pd.read_csv("ProvenanceCards/dataset/questions/questions_bench_2.csv")
ANSWERS["Answers"] = answers
ANSWERS.to_csv(f"ProvenanceCards/dataset/answers/template_v6/bench2/fromjsonl/{MODEL}.csv")



