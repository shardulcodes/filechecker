import os

# === Flask App Config ===
UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'
ALLOWED_EXTENSIONS = {'exe', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'png', 'txt', 'zip'}

# === VirusTotal API ===
# 👉 Get your key from https://www.virustotal.com/gui/user/apikey
VIRUSTOTAL_API_KEY = os.getenv('VT_API_KEY', 'b72f829f94e9f3d6838b070306628332c81bf430af2e175cb4bdaa7e508a572a')

# === PDF Report Options (pdfkit) ===
PDF_OPTIONS = {
    'encoding': 'UTF-8',
    'enable-local-file-access': None
}

# === Other Settings ===
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB limit for uploads

# === Security Options ===
DELETE_UPLOAD_AFTER_ANALYSIS = True
