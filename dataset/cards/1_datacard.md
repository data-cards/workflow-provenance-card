---
license: apache-2.0
task_categories:
- question-answering
language:
- en
tags:
- medical
pretty_name: ChatDoctor
size_categories:
- 100K<n<1M
---
This dataset was formed from the three data sources from the ChatDoctor work.

100k real conversations between patients and doctors from HealthCareMagic.com HealthCareMagic-100k. - ADDED

10k real conversations between patients and doctors from icliniq.com icliniq-10k. - ADDED

5k generated conversations between patients and physicians from ChatGPT GenMedGPT-5k and disease database. - NOT ADDED (because of the data created by LLM, but you could add it manually)


data sample:
```json
{'instruction': "If you are a doctor, please answer the medical questions based on the patient's description.",
 'input': "I woke up this morning feeling the whole room is spinning when i was sitting down. I went to the bathroom walking unsteadily, as i tried to focus i feel nauseous. I try to vomit but it wont come out.. After taking panadol and sleep for few hours, i still feel the same.. By the way, if i lay down or sit down, my head do not spin, only when i want to move around then i feel the whole world is spinning.. And it is normal stomach discomfort at the same time? Earlier after i relieved myself, the spinning lessen so i am not sure whether its connected or coincidences.. Thank you doc!",
 'output': "Hi, Thank you for posting your query. The most likely cause for your symptoms is benign paroxysmal positional vertigo (BPPV), a type of peripheral vertigo. In this condition, the most common symptom is dizziness or giddiness, which is made worse with movements. Accompanying nausea and vomiting are common. The condition is due to problem in the ear, and improves in a few days on own. Betahistine tablets would help relieve your symptoms. Doing vestibular rehabilitation or adaptation exercises would prevent the recurrence of these symptoms. An ENT evaluation would also help. I hope it helps. Best wishes, Chat Doctor. "}
```

```
@article{li2023chatdoctor,
  title={ChatDoctor: A Medical Chat Model Fine-Tuned on a Large Language Model Meta-AI (LLaMA) Using Medical Domain Knowledge},
  author={Li, Yunxiang and Li, Zihan and Zhang, Kai and Dan, Ruilong and Jiang, Steve and Zhang, You},
  journal={Cureus},
  volume={15},
  number={6},
  year={2023},
  publisher={Cureus}
}
```