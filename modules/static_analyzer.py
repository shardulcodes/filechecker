import subprocess
import math

def calculate_entropy(filepath):
    with open(filepath, 'rb') as f:
        byteArr = list(f.read())
        fileSize = len(byteArr)
        freqList = [0] * 256
        for b in byteArr:
            freqList[b] += 1
        entropy = 0.0
        for freq in freqList:
            if freq > 0:
                freq = float(freq) / fileSize
                entropy -= freq * math.log(freq, 2)
        return round(entropy, 3)

def extract_strings(filepath):
    result = subprocess.run(['strings', filepath], capture_output=True, text=True)
    return result.stdout[:1000]  # Limit preview

def analyze_file(filepath):
    entropy = calculate_entropy(filepath)
    strings = extract_strings(filepath)
    return {
        'entropy': entropy,
        'suspicious_strings_preview': strings
    }
