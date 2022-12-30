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


def form_html_order(
     part_html_order,
     src_image,
     title,
     result_file_name="_robot.html"):
    with open(result_file_name, "w") as file:
        template_result = read_file(HTML_TEMPLATE)

        part_html_order = re.sub(
            "(?s)<button.*?order-another.*</button>", "", part_html_order)

        result = re.sub(
            r"\{template_title}",
            f"Order Receipt: {title}",
            template_result)
        result = re.sub(r"\{template_order\}", part_html_order, result)
        result = re.sub(r"\{template_src_img\}", src_image, result)

        file.write(result)


def form_pdf_order(html_file_name, pdf_file_name):
    path = os.path.abspath(html_file_name)
    converter.convert(
        path,
        pdf_file_name,
        print_options={"preferCSSPageSize": True})


def read_file(file_name: str):
    result = None
    try:
        with open(file_name, encoding="utf-8") as file:
            result = file.read()
    except Exception as ex:
        print(f"Exception: {ex}")
        raise
    return result


if __name__ == "__main__":
    receipt_number = "RSB-ROBO-ORDER-S8ABFHTBFB"
    part_order_html = """
    <div id="order-completion">
        <div id="receipt" class="alert alert-success" role="alert">
            <h3>Receipt</h3>
            <div>2022-12-28T15:06:17.769Z</div>
            <p class="badge badge-success">RSB-ROBO-ORDER-S8ABFHTBFB</p>
            <p>Address 123</p>
            <div id="parts" class="alert alert-light" role="alert">
                <div>Head: 1</div>
                <div>Body: 2</div>
                <div>Legs: 3</div>
            </div>
            <p>Thank you for your order! We will ship your robot to you as soon
            as our warehouse robots gather the parts you ordered!
            You will receive your robot in no time!</p>
        </div>
    </div>"""
    form_html_order(
        part_order_html,
        "preview_robot.png",
        receipt_number,
        f"{receipt_number}_robot.html")
    form_pdf_order(
        f"{receipt_number}_robot.html",
        f"{receipt_number}_robot.pdf")
