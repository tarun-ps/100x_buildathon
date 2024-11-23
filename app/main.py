from tasks.core import generate_code, preliminary_analyse, generate_questions, \
    generate_svg, generate_animated_svg, generate_animated_video, pick_graph_type, \
    eliminate_unimportant_columns
# from dotenv import load_dotenv

# load_dotenv("dev.env")

def main():
    preliminary_analyse_res = preliminary_analyse("data/raw.csv")
    print(preliminary_analyse_res)
    eliminate_unimportant_columns("data/raw.csv", "data/test.csv", preliminary_analyse_res.columns)
    generate_questions_res = generate_questions(preliminary_analyse_res.domain, 
                                                preliminary_analyse_res.columns, 
                                                "data/test.csv")
    print(generate_questions_res)
    for i,question in enumerate(generate_questions_res.questions):
        generate_code_res = generate_code(preliminary_analyse_res.domain, 
                                          preliminary_analyse_res.columns, question, 
                                          "data/test.csv", f"code_{i}.py", 
                                          f"data/transformed_{i}.csv")
        exec(generate_code_res.code)
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

if __name__ == "__main__":
    main()