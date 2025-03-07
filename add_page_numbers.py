import fitz

def is_overlapping(rect1, rect2):
    return rect1.intersects(rect2)

def add_page_numbers(input_pdf, output_pdf, prefix="Page", start_page=1, position="BR"):
    doc = fitz.open(input_pdf)
    position_map = {
        "BR": (1, 1),
        "BL": (0, 1), 
        "TR": (1, 0), 
        "TL": (0, 0),
    }

    if position not in position_map:
        raise ValueError("Invalid position. Use one of 'BR', 'BL', 'TR', 'TL'.")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        original_rotation = page.rotation

        page.set_rotation(0)

        position_factor = position_map[position]

        page_width = page.rect.width
        page_height = page.rect.height

        x_pos = page_width * position_factor[0]
        y_pos = page_height * position_factor[1]
        text_margin = 100 
        top_margin = 50 if position == 'TL' else 30

        if position == "BR":
            x_pos = page_width - text_margin
            y_pos = page_height - top_margin
        elif position == "BL":
            x_pos = text_margin - 60
            y_pos = page_height - 20
        elif position == "TR":
            x_pos = page_width - text_margin
            y_pos = text_margin - 60
        elif position == "TL":
            x_pos = text_margin-60
            y_pos = top_margin

        page_number_rect = fitz.Rect(x_pos, y_pos, x_pos + 100, y_pos + 20)

        overlap = False
        for block in page.get_text("dict")["blocks"]:
            if block['type'] == 0: 
                for line in block["lines"]:
                    for span in line["spans"]:
                        existing_text_rect = fitz.Rect(span['bbox'])
                        if is_overlapping(page_number_rect, existing_text_rect):
                            overlap = True
                            break
                    if overlap:
                        break
                if overlap:
                    break

        if overlap:
            y_pos -= 30

        text = f"{prefix} {start_page + page_num}"
        fontsize = 12
        page.insert_text(
            (x_pos, y_pos), text, fontsize=fontsize
        )
        page.set_rotation(original_rotation)
    doc.save(output_pdf)

add_page_numbers("./test.pdf", "output_with_page_numbers.pdf", prefix="Page", start_page=1, position="BR")
