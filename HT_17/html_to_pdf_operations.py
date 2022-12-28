# html_to_pdf_operations.py
"""
Формування pdf файла заказу на основі форми
 отриманої із сайта
https://robotsparebinindustries.com/
"""
import os
import re

from pyhtml2pdf import converter


HTML_TEMPLATE = "order_template.html"


def form_html_order(part_html_order, src_image, title, result_file_name="_robot.html"):
    with open(result_file_name, "w") as file:
        template_result = read_file(HTML_TEMPLATE)

        part_html_order = re.sub("(?s)<button.*?order-another.*</button>", "", part_html_order)

        result = re.sub(r"\{template_title\}", f"Order Receipt: {title}", template_result)
        result = re.sub(r"\{template_order\}", part_html_order, result)
        result = re.sub(r"\{template_src_img\}", src_image, result)

        file.write(result)


def form_pdf_order(html_file_name, pdf_file_name):
    path = os.path.abspath(html_file_name)
    converter.convert(f'file:///{path}', pdf_file_name)


def read_file(file_name: str):
    result = None
    try:
        with open(file_name, encoding="utf-8") as file:
            result = file.read()
    except Exception as ex:
        print(f"Exception: {ex}")
        raise
    return result
