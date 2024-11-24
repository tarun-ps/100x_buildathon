import json
import os

def get_all_tasks():
    ret = []
    for task_id in os.listdir("user_data"):
        domain = get_task_domain(task_id)
        ret.append({"id": task_id, "domain": domain})
    return ret

def get_task_domain(task_id: str):
    metadata = json.load(open(f"user_data/{task_id}/metadata.json"))
    return metadata["preliminary_analyse"]["domain"]

def get_task_data(task_id: str):
    metadata = json.load(open(f"user_data/{task_id}/metadata.json"))
    files = os.listdir(f"user_data/{task_id}/output")
    videos = [file for file in files if file.endswith(".mp4")]
    ret = {}
    ret["id"] = task_id
    ret["domain"] = metadata["preliminary_analyse"]["domain"]
    questions = metadata["questions"]["questions"]
    ret_questions = []
    for i, question in enumerate(questions):
        if f"output_{i}.mp4" in videos:
            ret_questions.append({"question": question, "video": f"{task_id}/video/{i}", "status": "ready"})
        else:
            ret_questions.append({"question": question, "video": None, "status": "processing"})
    ret["questions"] = ret_questions
    return ret
