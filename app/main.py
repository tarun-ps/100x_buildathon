from tasks.core import generate_animated_video_horizontal_bar, generate_animated_video_pie_chart, generate_code, preliminary_analyse, generate_questions, \
    generate_svg, generate_animated_svg, generate_animated_video, pick_graph_type, \
    eliminate_unimportant_columns, GraphType
import os
# from dotenv import load_dotenv

# load_dotenv("dev.env")

def main():
    preliminary_analyse_res = preliminary_analyse("data/tech-employer-totals.csv")
    print(preliminary_analyse_res)
    eliminate_unimportant_columns("data/tech-employer-totals.csv", "data/test.csv", preliminary_analyse_res.columns)
    generate_questions_res = generate_questions(preliminary_analyse_res.domain, 
                                                preliminary_analyse_res.columns, 
                                                "data/test.csv")
    print(generate_questions_res)
    for i,question in enumerate(generate_questions_res.questions):
        generate_code_res = generate_code(preliminary_analyse_res.domain, 
                                          preliminary_analyse_res.columns, question, 
                                          "data/test.csv", f"code_{i}.py", 
                                          f"data/transformed_{i}.csv")
        while True:
            try:
                exec(generate_code_res.code)
                break
            except Exception as e:
                generate_code_res = generate_code(preliminary_analyse_res.domain, 
                                          preliminary_analyse_res.columns, question, 
                                          "data/test.csv", f"code_{i}.py", 
                                          f"data/transformed_{i}.csv")
        pick_graph_type_res = pick_graph_type(question, 
                                          f"data/transformed_{i}.csv")
        print(pick_graph_type_res)
        generate_svg_res = generate_svg(question, 
                                    f"data/transformed_{i}.csv", pick_graph_type_res.graph_type,
                                    f"graph_{i}.svg")
        print(generate_svg_res)
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
    generate_pie_chart_video()
    #generate_all_videos()