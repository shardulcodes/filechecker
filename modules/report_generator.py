import os
from datetime import datetime
from flask import render_template
from jinja2 import Environment, FileSystemLoader
import pdfkit  # Optional, if PDF needed


def generate_html_report(data, filepath):
    """
    Generates an HTML report using the given data and saves it to reports folder.
    """
    filename = os.path.basename(filepath)
    report_id = filename + "_report.html"
    report_path = os.path.join('reports', report_id)

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report_template.html')

    rendered = template.render(data=data, generated=datetime.now())

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

    return report_path  # e.g., reports/uuid_filename_report.html


def generate_pdf_report(html_path):
    """
    Generates a PDF from the given HTML file using pdfkit.
    Requires wkhtmltopdf to be installed and configured.
    """
    pdf_path = html_path.replace(".html", ".pdf")

    try:
        pdfkit.from_file(html_path, pdf_path)
        return pdf_path
    except Exception as e:
        print(f"[!] PDF generation failed: {e}")
        return None
