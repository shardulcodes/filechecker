from flask import Flask, request, render_template, send_file, redirect, url_for
from modules import metadata_extractor, hash_checker, static_analyzer, heuristic_engine, report_generator
from werkzeug.utils import secure_filename
import os, uuid, json

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB upload limit

# Ensure necessary folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# -------------------------
# ROUTES
# -------------------------

# Home Route - Upload Form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "No file uploaded", 400

        # Save uploaded file
        file_id = str(uuid.uuid4())
        filename = file_id + "_" + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Run full analysis
        result = {}
        result.update(metadata_extractor.extract_metadata(filepath))
        result.update(hash_checker.check_hashes(filepath))
        result.update(static_analyzer.analyze_file(filepath))
        result.update(heuristic_engine.run_heuristics(result))

        # Save JSON Report
        json_path = os.path.join(REPORT_FOLDER, file_id + '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)

        # Generate HTML & PDF Reports
        html_path = report_generator.generate_html_report(result, filepath)
        report_generator.generate_pdf_report(html_path)

        return redirect(url_for('dashboard', report_id=file_id))

    return render_template('index.html', report_id=None)


# Dashboard Route - After Analysis
@app.route('/dashboard/<report_id>')
def dashboard(report_id):
    json_path = os.path.join(REPORT_FOLDER, report_id + '.json')
    html_path = os.path.join(REPORT_FOLDER, report_id + '_report.html')
    pdf_path = os.path.join(REPORT_FOLDER, report_id + '.pdf')

    if not os.path.exists(json_path):
        return "Report not found", 404

    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    return render_template(
        'dashboard.html',
        data=data,
        report_id=report_id,
        html_available=os.path.exists(html_path),
        pdf_available=os.path.exists(pdf_path)
    )


# View HTML Report in Browser
@app.route('/view/<report_id>')
def view_report(report_id):
    path = os.path.join(REPORT_FOLDER, report_id + '_report.html')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return f.read()
    return "HTML report not found", 404


# Download PDF Report
@app.route('/download/pdf/<report_id>')
def download_pdf(report_id):
    path = os.path.join(REPORT_FOLDER, report_id + '.pdf')
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "PDF report not found", 404


# Download JSON Report
@app.route('/download/json/<report_id>')
def download_json(report_id):
    path = os.path.join(REPORT_FOLDER, report_id + '.json')
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "JSON report not found", 404


# Future Route: Dynamic Analysis Placeholder
@app.route('/dynamic')
def dynamic_analysis():
    return render_template('dynamic.html', report_id=None)


# Future Route: Reports Listing Placeholder
@app.route('/reports')
def reports():
    report_files = [f for f in os.listdir(REPORT_FOLDER) if f.endswith('.json')]
    reports = []

    for file in sorted(report_files, reverse=True):  # latest first
        report_id = file.replace('.json', '')
        json_path = os.path.join(REPORT_FOLDER, file)
        html_path = os.path.join(REPORT_FOLDER, f"{report_id}_report.html")
        pdf_path = os.path.join(REPORT_FOLDER, f"{report_id}.pdf")

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            reports.append({
                'id': report_id,
                'filename': data.get('filename'),
                'date': data.get('created') or data.get('modified') or '',
                'has_html': os.path.exists(html_path),
                'has_pdf': os.path.exists(pdf_path),
            })
        except Exception:
            continue  # skip corrupted reports

    return render_template('reports.html', reports=reports)


# Health Check
@app.route('/health')
def health():
    return "OK", 200


# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
