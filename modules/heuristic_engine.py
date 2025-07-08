import os
import re

def run_heuristics(info):
    score = 0
    reasons = []

    # ---- RULE 1: High Entropy ----
    entropy = info.get('entropy')
    if isinstance(entropy, (int, float)) and entropy > 7.5:
        score += 30
        reasons.append(f"High entropy ({entropy:.2f}) indicates potential obfuscation or packed file.")

    # ---- RULE 2: Suspicious Strings (Command & Malware Tools) ----
    suspicious_preview = info.get('suspicious_strings_preview', "").lower()
    indicators = [
        'powershell', 'cmd.exe', 'curl', 'wget', 'mshta', 'vbs', 'jscript',
        'base64', 'eval(', 'document.write', 'CreateObject', 'shellcode'
    ]
    matched = [term for term in indicators if term in suspicious_preview]
    if matched:
        score += 40
        reasons.append(f"Suspicious keywords found in file strings: {', '.join(matched)}")

    # ---- RULE 3: VirusTotal Detection ----
    vt_hits = info.get('VirusTotal_Detected_Engines', 0)
    if isinstance(vt_hits, int) and vt_hits > 5:
        score += 50
        reasons.append(f"VirusTotal detected {vt_hits} engines reporting this file as malicious.")

    # ---- RULE 4: Dangerous File Extensions ----
    filename = info.get('filename', "")
    ext = os.path.splitext(filename)[1].lower()
    dangerous_exts = ['.exe', '.bat', '.cmd', '.vbs', '.js', '.scr', '.ps1']
    if ext in dangerous_exts:
        score += 20
        reasons.append(f"File extension '{ext}' is commonly associated with executables or scripts.")

    # ---- RULE 5: Potentially Embedded Executable Content ----
    mime = info.get('mime_type', "").lower()
    if re.search(r'application/x-msdownload|application/octet-stream', mime):
        score += 25
        reasons.append(f"MIME type '{mime}' suggests binary/executable content.")

    # ---- Rule 6: Signature Mismatch (optional if you calculate it) ----
    if info.get("signature_mismatch") is True:
        score += 25
        reasons.append("File signature does not match its extension (possible spoofing).")

    # Cap total score to 100
    final_score = min(score, 100)

    return {
        'suspicion_score': final_score,
        'heuristic_flags': reasons,
        'is_suspicious': final_score >= 50  # Add boolean flag
    }
