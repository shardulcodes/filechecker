import os
from jinja2 import Template
from datetime import datetime

def generate_html_report(data, filepath):
    filename = os.path.basename(filepath)
    report_id = filename + "_report.html"
    report_path = os.path.join('reports', report_id)

    with open('templates/report_template.html', encoding='utf-8') as f:
        template = Template(f.read())

    rendered = template.render(data=data, generated=datetime.now())

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

    return report_path  # returning path to HTML
