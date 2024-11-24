import json
from tasks.core import generate_animated_video_horizontal_bar, generate_animated_video_pie_chart, generate_code, preliminary_analyse, generate_questions, \
    generate_svg, generate_animated_svg, generate_animated_video, pick_graph_type, \
    eliminate_unimportant_columns, GraphType
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
# from dotenv import load_dotenv

# load_dotenv("dev.env")
def cleanup_folders():
    os.system("rm -rf output/*")
    os.system("rm -rf code/*")
    os.system("rm -rf frames/*")
    os.system("rm -rf data/transformed_*.csv")

def main():
    cleanup_folders()
    preliminary_analyse_res = preliminary_analyse("data/tech-employer-totals.csv")
    eliminate_unimportant_columns("data/tech-employer-totals.csv", "data/test.csv", preliminary_analyse_res.columns)
    generate_questions_res = generate_questions(preliminary_analyse_res.domain, 
                                                preliminary_analyse_res.columns, 
                                                "data/test.csv")
    metadata = {
        "preliminary_analyse": preliminary_analyse_res.to_dict(),
        "questions": generate_questions_res.to_dict(),
    }
    with open("data/metadata.json", "w") as f:
        json.dump(metadata, f)

    for i,question in enumerate(generate_questions_res.questions):
        generate_code_res = generate_code(preliminary_analyse_res.domain, 
                                          preliminary_analyse_res.columns, question, 
                                          "data/test.csv", f"code/code_{i}.py", 
                                          f"data/transformed_{i}.csv")
        retry = 0
        while retry < 3:
            try:
                exec(generate_code_res.code)
                break
            except Exception as e:
                retry += 1
                generate_code_res = generate_code(preliminary_analyse_res.domain, 
                                          preliminary_analyse_res.columns, question, 
                                          "data/test.csv", f"code/code_{i}.py", 
                                          f"data/transformed_{i}.csv")
        pick_graph_type_res = pick_graph_type(question, 
                                          f"data/transformed_{i}.csv")
        print(pick_graph_type_res)
        generate_svg_res = generate_svg(question, 
                                    f"data/transformed_{i}.csv", pick_graph_type_res.graph_type,
                                    f"output/graph_{i}.svg")
        print(generate_svg_res)
        generate_animated_video(f"output/graph_{i}.svg", f"output/output_{i}.mp4", pick_graph_type_res.graph_type)
    # generate_animated_svg("graph.svg")
    # generate_animated_video("graph.svg")
    # 
    # print(res)
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
    #main()
    generate_animated_video(f"output/graph_1.svg", f"output/output_1.mp4", GraphType.BAR)
    # generate_svg_res = generate_svg("question", 
    #                                 f"data/transformed_3.csv", GraphType.HORIZONTAL_BAR,
    #                                 f"output/graph_3.svg")
    # print(generate_svg_res)
