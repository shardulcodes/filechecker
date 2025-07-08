import os
import mimetypes
from datetime import datetime

def extract_metadata(filepath):
    stat = os.stat(filepath)
    return {
        'filename': os.path.basename(filepath),
        'filetype': mimetypes.guess_type(filepath)[0],
        'filesize': stat.st_size,
        'created': str(datetime.fromtimestamp(stat.st_ctime)),
        'modified': str(datetime.fromtimestamp(stat.st_mtime))
    }
