import json
import uuid
from schemas.core import ExtractCSVFromTextResponse
from tasks.core import generate_animated_video_horizontal_bar, generate_animated_video_pie_chart, generate_videos_for_text_input, \
    preliminary_analyse, generate_questions, \
    eliminate_unimportant_columns, generate_code_and_videos, extract_csv_from_text
import os
# from dotenv import load_dotenv

# load_dotenv("dev.env")
def cleanup_folders():
    os.system("rm -rf output/*")
    os.system("rm -rf code/*")
    os.system("rm -rf frames/*")
    os.system("rm -rf data/transformed_*.csv")

def process_text(text: str, task_id: str):
    create_task_folder(task_id)
    res = extract_csv_from_text(text, task_id)
    domain = res.title
    json_data = {"preliminary_analyse": {"domain": domain}, "questions": {"questions": [text[:100]]}}
    with open(f"user_data/{task_id}/metadata.json", "w") as f:
        json.dump(json_data, f)
    return process_user_text(res, task_id)

def process_user_text(res: ExtractCSVFromTextResponse, task_id: str):
    generate_videos_for_text_input.delay(task_id, res.title)
    return {"id": task_id, "status": "processing", "domain": res.title[:100]}

def process(task_id: str):
    create_task_folder(task_id)
    return process_csv(f"user_data/{task_id}/raw.csv", task_id)

def create_task_folder(task_id: str):
    os.makedirs(f"user_data/{task_id}", exist_ok=True)
    os.makedirs(f"user_data/{task_id}/code", exist_ok=True)
    os.makedirs(f"user_data/{task_id}/frames", exist_ok=True)
    os.makedirs(f"user_data/{task_id}/output", exist_ok=True)

def process_csv(csv_file_path: str, task_id: str):
    cleanup_folders()
    preliminary_analyse_res = preliminary_analyse(csv_file_path)
    eliminate_unimportant_columns(csv_file_path, f"user_data/{task_id}/transformed.csv", preliminary_analyse_res.columns)
    generate_questions_res = generate_questions(preliminary_analyse_res.domain, 
                                                preliminary_analyse_res.columns, 
                                                f"user_data/{task_id}/transformed.csv")
    metadata = {
        "preliminary_analyse": preliminary_analyse_res.to_dict(),
        "questions": generate_questions_res.to_dict(),
    }
    with open(f"user_data/{task_id}/metadata.json", "w") as f:
        json.dump(metadata, f)

    generate_code_and_videos.delay(task_id, json.dumps(preliminary_analyse_res.to_dict()), json.dumps(generate_questions_res.to_dict()))
    return {"id": task_id, "status": "processing", "domain": preliminary_analyse_res.domain}


def generate_pie_chart_video() -> str:
    csv = "data/transformed_0.csv"
    # generate_svg_res = generate_svg("", csv, 
    #                                 GraphType.PIE, "graph_pie.svg")
    generate_animated_video_pie_chart("graph_pie.svg")
    ffmpeg_command = f"ffmpeg -r 30 -f image2 -s 500x500 -i frames/frame_%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p output_pie.mp4"
    print(ffmpeg_command)
    os.system(ffmpeg_command)
    print(f"Generated video for pie chart")
    return 

def generate_all_videos():
    for i in range(5):
        generate_animated_video_horizontal_bar(f"graph_{i}.svg")
        print(f"Generated frames for {i}")
        ffmpeg_command = f"ffmpeg -r 30 -f image2 -s 500x500 -i frames/frame_%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p output{i}.mp4"
        print(ffmpeg_command)
        os.system(ffmpeg_command)
        print(f"Generated video for {i}")

   
if __name__ == "__main__":
    task_id = str(uuid.uuid4())
    # create_task_folder(task_id)
    # os.system(f"cp data/actor-metrics.csv user_data/{task_id}/raw.csv")
    # process(task_id)
    #generate_animated_video(f"output/graph_1.svg", f"output/output_1.mp4", GraphType.BAR)
    # generate_svg_res = generate_svg("question", 
    #                                 f"data/transformed_3.csv", GraphType.HORIZONTAL_BAR,
    #                                 f"output/graph_3.svg")
    # print(generate_svg_res)
    t = "20% of users own an iPhone, 50% own a Samsung, and the rest own a variety of brands"
    print(process_text(t, task_id))
