from flask import Flask, request, render_template, send_file
from modules import metadata_extractor, hash_checker, static_analyzer, heuristic_engine, report_generator
import os, uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        file_id = str(uuid.uuid4())
        filepath = os.path.join(UPLOAD_FOLDER, file_id + "_" + file.filename)
        file.save(filepath)

        result = {}
        result.update(metadata_extractor.extract_metadata(filepath))
        result.update(hash_checker.check_hashes(filepath))
        result.update(static_analyzer.analyze_file(filepath))
        result.update(heuristic_engine.run_heuristics(result))

        report_path = report_generator.generate_html_report(result, filepath)
        with open(report_path, encoding='utf-8') as f:
            return f.read()



    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
