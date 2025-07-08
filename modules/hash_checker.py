import hashlib
import requests
from config import VIRUSTOTAL_API_KEY

def generate_hashes(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
        return {
            'md5': hashlib.md5(data).hexdigest(),
            'sha1': hashlib.sha1(data).hexdigest(),
            'sha256': hashlib.sha256(data).hexdigest()
        }

def check_virustotal(sha256_hash):
    url = f"https://www.virustotal.com/api/v3/files/{sha256_hash}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        json_resp = resp.json()
        return {
            'virustotal_positives': json_resp['data']['attributes']['last_analysis_stats']['malicious'],
            'virustotal_link': f"https://www.virustotal.com/gui/file/{sha256_hash}"
        }
    return {'virustotal': 'Not found or error'}

def check_hashes(filepath):
    hashes = generate_hashes(filepath)
    vt_result = check_virustotal(hashes['sha256'])
    return {**hashes, **vt_result}
