"""Core PDF conversion logic. Extracts text from colored-background PDFs
and renders it as black text on a white page."""

import fitz  # pymupdf


# pymupdf built-in Base14 font mapping
_FONT_MAP = {
    (True, True): "hebi",    # bold + italic
    (True, False): "hebo",   # bold
    (False, True): "heit",   # italic
    (False, False): "helv",  # regular
}


def convert(input_path: str, output_path: str) -> None:
    """Convert a PDF to black text on white background.

    Args:
        input_path: Path to source PDF.
        output_path: Path for the converted PDF.
    """
    src = fitz.open(input_path)
    doc = fitz.open()

    for src_page in src:
        width = src_page.rect.width
        height = src_page.rect.height
        page = doc.new_page(width=width, height=height)

        # Extract text with positional data
        blocks = src_page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] != 0:  # text blocks only
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue

                    origin = fitz.Point(span["origin"][0], span["origin"][1])
                    size = span["size"]
                    flags = span["flags"]

                    is_bold = bool(flags & (1 << 4))
                    is_italic = bool(flags & (1 << 1))
                    fontname = _FONT_MAP[(is_bold, is_italic)]

                    page.insert_text(
                        origin,
                        text,
                        fontsize=size,
                        fontname=fontname,
                        color=(0, 0, 0),
                    )

        # Redraw vector drawings (table borders, lines) in black
        paths = src_page.get_drawings()
        for path in paths:
            # Only keep stroked paths (lines/borders), skip fills (backgrounds)
            if path.get("fill"):
                continue
            if not path.get("color"):
                continue

            shape = page.new_shape()
            for item in path["items"]:
                op = item[0]
                if op == "l":  # line
                    shape.draw_line(item[1], item[2])
                elif op == "re":  # rectangle
                    shape.draw_rect(item[1])
                elif op == "c":  # cubic bezier
                    shape.draw_bezier(item[1], item[2], item[3], item[4])
                elif op == "qu":  # quad
                    shape.draw_quad(item[1])

            shape.finish(
                color=(0, 0, 0),
                width=path.get("width", 0.5),
            )
            shape.commit()

    doc.save(output_path)
    doc.close()
    src.close()
