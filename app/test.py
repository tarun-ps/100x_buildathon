from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
def render_svg(input_svg: str, output_png: str) -> None:
    svg_content = svg2rlg(input_svg)
    renderPM.drawToFile(svg_content, output_png, fmt='PNG')

if __name__ == "__main__":
    render_svg('frames/flattened_test.svg', 'frames/flattened_test.png')
