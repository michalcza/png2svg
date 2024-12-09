import argparse
from PIL import Image
import potrace
import os

def png_to_svg(input_file):
    output_file = os.path.splitext(input_file)[0] + ".svg"
    img = Image.open(input_file).convert("L")
    bw_img = img.point(lambda x: 0 if x < 128 else 1, "1")
    bitmap = potrace.Bitmap(bw_img)
    path = bitmap.trace()
    with open(output_file, "w") as svg:
        svg.write('<?xml version="1.0" standalone="no"?>\n')
        svg.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        svg.write(f'<svg xmlns="http://www.w3.org/2000/svg" version="1.0" width="{img.width}" height="{img.height}">\n')

        for curve in path:
            svg.write('<path d="')
            for segment in curve.segments:
                if segment.is_corner:
                    svg.write(f'L {segment.c.x} {segment.c.y} ')
                else:
                    svg.write(f'C {segment.c1.x} {segment.c1.y} {segment.c2.x} {segment.c2.y} {segment.c.x} {segment.c.y} ')
            svg.write('" fill="black" stroke="none" />\n')

        svg.write('</svg>\n')

    print(f"SVG saved as: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a PNG file to an SVG file using Potrace.")
    parser.add_argument("input_file", help="Path to the input PNG file")
    args = parser.parse_args()
    png_to_svg(args.input_file)
