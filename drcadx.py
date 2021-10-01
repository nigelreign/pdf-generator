from jinja2 import Environment, FileSystemLoader
import os
import pdfkit
from PyPDF2 import PdfFileWriter, PdfFileReader
import random
import string


def generate_pdf(
    heat_map: str,
    results: list,
):
    """Create Results PDF

    Args:
        results: results,

    """

    pdf_name = "".join(
        random.choice(string.ascii_uppercase + string.digits) for i in range(8)
    )

    # pass variables to our html template
    env = Environment(loader=FileSystemLoader(os.getcwd()))
    template = env.get_template("templates/drcadx.html")
    html = template.render(
        heat_map=heat_map,
        results=results,
    )

    # save the generated html file
    file = open("templates/temp-generated-html/" + pdf_name + ".html", "w")
    file.write(html)
    file.close()

    options = {
        "page-size": "Letter",
        "margin-top": "0.0in",
        "margin-right": "0.0in",
        "margin-bottom": "0.0in",
        "margin-left": "0.0in",
        "encoding": "UTF-8",
        # '--header-html': 'header.html',
        "custom-header": [("Accept-Encoding", "gzip")],
        "no-outline": None,
    }
    # convert the html file to a pdf file
    pdfkit.from_file(
        "templates/temp-generated-html/" + pdf_name + ".html",
        "generated-pdf/" + pdf_name + ".pdf",
        options=options,
    )

    os.remove("templates/temp-generated-html/" + pdf_name + ".html")


heat_map = "data:image/jpeg;base64,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"

generate_pdf(
    heat_map=heat_map,
    results=[
        {"predictions": "test name", "probability": "20%"},
        {"predictions": "test name2", "probability": "20%"},
        {"predictions": "test name3", "probability": "20%"},
        {"predictions": "test name3", "probability": "20%"},
        {"predictions": "test name3", "probability": "20%"},
        {"predictions": "test name3", "probability": "20%"},
        {"predictions": "test name3", "probability": "20%"},
        {"predictions": "test name3", "probability": "20%"},
        {"predictions": "test name3", "probability": "20%"},
    ],
)
