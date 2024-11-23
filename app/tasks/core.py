from enum import Enum
from pydantic import BaseModel
from openai import OpenAI
from settings import OPENAI_O1_PREVIEW_MODEL, \
    OPENAI_API_KEY, OPENAI_API_BASE_URL, \
    PRELIMINARY_ANALYSE_SYSTEM_PROMPT, \
    PRELIMINARY_ANALYSE_USER_PROMPT, \
    OPENAI_GPT4_O_MODEL, \
    GENERATE_QUESTIONS_SYSTEM_PROMPT, \
    GENERATE_QUESTIONS_USER_PROMPT, \
    PICK_GRAPH_TYPE_SYSTEM_PROMPT, \
    PICK_GRAPH_TYPE_USER_PROMPT, \
    GENERATE_CODE_SYSTEM_PROMPT, \
    GENERATE_CODE_USER_PROMPT
import json
import pandas as pd
import pygal
from pygal.style import Style
import numpy as np
from bs4 import BeautifulSoup
import cairosvg
from xml.etree import ElementTree as ET
import os
from PIL import Image
client = OpenAI()

class PreliminaryAnalyseResponse(BaseModel):
    domain: str
    columns: list[str]

class GenerateQuestionsResponse(BaseModel):
    questions: list[str]

class PickGraphTypeResponse(BaseModel):
    graph_type: str
    reason: str

class GenerateCodeResponse(BaseModel):
    code: str

class GraphType(Enum):
    LINE = "line"
    HORIZONTAL_LINE = "horizontal_line"
    STACKED_LINE = "stacked_line"
    BAR = "bar"
    STACKED_BAR = "stacked_bar"
    HORIZONTAL_BAR = "horizontal_bar"
    PIE = "pie"
    DONUT = "donut"

def preliminary_analyse(file_path: str) -> PreliminaryAnalyseResponse:
    df = pd.read_csv(file_path)
    data_summary = df.head().to_string()
    data_description = df.describe().to_string()
    #print(data_summary)
    completion = client.beta.chat.completions.parse(
        model=OPENAI_GPT4_O_MODEL,
        response_format=PreliminaryAnalyseResponse,
        messages=[
            {"role": "system", "content": PRELIMINARY_ANALYSE_SYSTEM_PROMPT},
            {"role": "user", "content": PRELIMINARY_ANALYSE_USER_PROMPT.format(data_summary, data_description)},
        ],
    )
    return PreliminaryAnalyseResponse.parse_obj(json.loads(completion.choices[0].message.content))

def eliminate_unimportant_columns(input_file_path: str, output_file_path: str, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(input_file_path)
    df = df[columns]
    df.to_csv(output_file_path, index=False)
    return

def generate_questions(domain: str, columns: list[str], file_path: str) -> GenerateQuestionsResponse:
    df = pd.read_csv(file_path)
    data_description = df.describe().to_string()
    data_summary = df.head().to_string()
    print(data_description)
    print(data_summary)
    completion = client.beta.chat.completions.parse(
        model=OPENAI_GPT4_O_MODEL,
        response_format=GenerateQuestionsResponse,
        messages=[
            {"role": "system", "content": GENERATE_QUESTIONS_SYSTEM_PROMPT},
            {"role": "user", "content": GENERATE_QUESTIONS_USER_PROMPT.format(domain, ",".join(columns), data_description, data_summary)},
        ],
    )
    return GenerateQuestionsResponse.parse_obj(json.loads(completion.choices[0].message.content))

def generate_code(domain: str, columns: list[str], question: str, 
                  file_path: str, output_file_path: str, output_data_file_path: str) -> GenerateCodeResponse:
    df = pd.read_csv(file_path)
    data_description = df.describe().to_string()
    data_sample = df.head().to_string()
    user_prompt = GENERATE_CODE_USER_PROMPT.format(domain=domain, 
                                                   columns=", ".join(columns), 
                                                   question=question, 
                                                   data_description=data_description, 
                                                   data_sample=data_sample,
                                                   output_path=output_data_file_path)
    completion = client.beta.chat.completions.parse(
        model=OPENAI_GPT4_O_MODEL,
        response_format=GenerateCodeResponse,
        messages=[
            {"role": "system", "content": GENERATE_CODE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    code_response = GenerateCodeResponse.parse_obj(json.loads(completion.choices[0].message.content))
    with open(output_file_path, "w") as f:
        f.write(code_response.code)
    return code_response

def pick_graph_type(question: str, file_path: str) -> PickGraphTypeResponse:
    df = pd.read_csv(file_path)
    #format df into a string
    data_description = df.to_string()
    chart_types = "\n".join([chart_type.value for chart_type in GraphType])
    user_prompt = PICK_GRAPH_TYPE_USER_PROMPT.format(question=question, \
                                                      data=data_description, \
                                                      chart_types=chart_types)
    completion = client.beta.chat.completions.parse(
        model=OPENAI_GPT4_O_MODEL,
        response_format=PickGraphTypeResponse,
        messages=[
            {"role": "system", "content": PICK_GRAPH_TYPE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return PickGraphTypeResponse.parse_obj(json.loads(completion.choices[0].message.content))
def transform_data():
    # Load the dataset
    # Load the data from the CSV file
    data = pd.read_csv("data/test.csv")

    # Ensure data is sorted by year and Gender equality Index to identify the top-ranked countries
    data = data.sort_values(by=["year", "Gender equality Index"], ascending=[True, False])

    # Group by year and take the top 5 countries with the highest Gender equality Index for each year
    top_countries_per_year = data.groupby("year").head(5)

    # Transform the dataset for visualization purposes
    # The first column should be the labels (years)
    # Other columns should represent values (Gender equality Index for the top countries)
    transformed_data = top_countries_per_year.pivot(index="year", columns="country", values="Gender equality Index")

    # Limit the number of columns (countries) to a maximum of 8, taking those with the highest mean index over all years
    top_countries = transformed_data.mean().nlargest(8).index
    transformed_data = transformed_data[top_countries]

    # Reset index to make the year column explicit
    transformed_data.reset_index(inplace=True)

    # Save the transformed dataframe to a CSV file
    transformed_data.to_csv("data/transformed.csv", index=False)
    print(transformed_data)

    print("Data transformation complete. Transformed data saved to 'data/transformed.csv'.")

def generate_svg(question: str, file_path: str, graph_type: str = "line", output_file_path: str = "graph.svg") -> str:
    custom_style = Style(
        font_family='googlefont:Raleway',
        transition='4000ms ease-in')
    df = pd.read_csv(file_path)
    if graph_type == "line":
        graph = pygal.Line(style=custom_style, interpolate='cubic')
    elif graph_type == "horizontal_line":
        graph = pygal.HorizontalLine(style=custom_style)
    elif graph_type == "stacked_line":
        graph = pygal.StackedLine(style=custom_style, interpolate='cubic')
    elif graph_type == "bar":
        graph = pygal.Bar(style=custom_style)
    elif graph_type == "stacked_bar":
        graph = pygal.StackedBar(style=custom_style)
    elif graph_type == "horizontal_bar":
        graph = pygal.HorizontalBar(style=custom_style)
    elif graph_type == "pie":
        graph = pygal.Pie(style=custom_style)
    elif graph_type == "donut":
        graph = pygal.Pie(style=custom_style, inner_radius=0.40)
    graph.title = question
    graph.x_labels = df[df.columns[0]]
    for column in df.columns[1:]:
        graph.add(column, df[column].replace([np.nan], None))
    graph.render_to_file(output_file_path)
    return output_file_path

def generate_animated_svg(svg_file_path: str) -> str:
    mask = "<mask id=\"reveal-mask\"> <rect x=\"0\" y=\"0\" width=\"0\" height=\"600\" fill=\"white\" id=\"mask-rect\"></rect></mask>"
    style = "<style> #mask-rect { animation: reveal 1s linear forwards;} @keyframes reveal { to { width: 800px; }}</style>"
    svg_output_path = svg_file_path.replace(".svg", "_animated.svg")
    with open(svg_file_path, "r") as file:
        svg = file.read()
    #get all the path nodes uder a g tag wioth class called "series" using beautifulsoup
    soup = BeautifulSoup(svg, "xml")
    mask  = BeautifulSoup(mask, "xml")
    #add mask as the first child of the svg tag in soup
    soup.svg.insert(0, mask)
    paths = soup.find_all("path", class_="line reactive nofill")
    for path in paths:
        print(path)
        path["mask"] = "url(#reveal-mask)"
    svg = soup.prettify()
    with open(svg_output_path, "w") as file:
        file.write(svg)

    html = f"<html><body>"+ svg + style + "</body></html>"
    with open(svg_output_path.replace(".svg", ".html"), "w") as file:
        file.write(html)
    return svg_output_path

def generate_animated_video(svg_file_path: str) -> str:
    mask = "<mask id=\"reveal-mask\"> <rect x=\"0\" y=\"0\" width=\"{width}\" height=\"600\" fill=\"white\" id=\"mask-rect\"></rect></mask>"
    with open(svg_file_path, "r") as file:
        svg = file.read()
    #get all the path nodes uder a g tag wioth class called "series" using beautifulsoup
    soup = BeautifulSoup(svg, "xml")
    mask  = BeautifulSoup(mask, "xml")
    #add mask as the first child of the svg tag in soup
    soup.svg.insert(0, mask)
    paths = soup.find_all("path", class_="line reactive nofill")
    for path in paths:
        path["mask"] = "url(#reveal-mask)"
    svg = soup.prettify()
    #convert svg to string
    svg_template = str(svg)
    final_width = 800
    total_frames = 60
    output_dir = "frames"
    os.makedirs(output_dir, exist_ok=True)
    for frame in range(total_frames):
        width = int(frame * (final_width / total_frames))
        svg_frame = svg_template.replace("{width}", str(width))
        frame_file = os.path.join(output_dir, f"frame_{frame:04d}.png")
        cairosvg.svg2png(bytestring=svg_frame, write_to=frame_file)
        print(f"Generated frame: {frame_file}")
    return output_dir
