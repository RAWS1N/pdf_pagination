import fitz

def is_overlapping(rect1, rect2):
    return rect1.intersects(rect2)

def add_page_numbers(input_pdf, output_pdf, prefix="Page", start_page=1, position="BR",border_color=(1,1,1)):
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
        page_width = page.rect.width
        page_height = page.rect.height
        text_box_width = 80
        text_box_height = 20
        text_box_rect = fitz.Rect(50, 50, 50 + text_box_width, 50 + text_box_height)

        page_number_text = f"{prefix} {start_page + page_num}"

        text_margin = 50 
        top_margin = 50 if position == 'TL' else 25
        
        if position == "BR":
            x_pos = page_width - text_margin - text_box_width 
            y_pos = page_height - top_margin - text_box_height 
        elif position == "BL":
            x_pos = text_margin - 20  
            y_pos = page_height - top_margin - text_box_height 
        elif position == "TR":
            x_pos = page_width - text_margin - text_box_width 
            y_pos = text_margin - 40 
        elif position == "TL":
            x_pos = text_margin - 20  
            y_pos = text_margin - 40 

        text_box_rect = fitz.Rect(x_pos, y_pos, x_pos + text_box_width, y_pos + text_box_height)

        page.draw_rect(
            text_box_rect,
            color=border_color, 
            fill=(1, 1, 1) 
        )

        page.insert_textbox(
            text_box_rect,
            page_number_text,
            fontsize=12,
            fontname="Times-Roman",
            align=1 
        )

        page.set_rotation(original_rotation)

    doc.save(output_pdf)

add_page_numbers("./test.pdf", "output_with_page_numbers.pdf", prefix="Page", start_page=1, position="BR",border_color=(0,0,0))
