import tempfile
import subprocess
import re
from dateutil import parser
import uuid
from django.conf import settings

def runProcess(exe):    
    retcode = subprocess.check_call(exe)
    return retcode

def webm(input_file, size):
    
    tmp_file = "%s.webm" % tempfile.mkstemp()[1]
    
    
    
    retcode = runProcess(["ffmpeg", "-i", input_file, "-quality", "good", "-cpu-used", "0", "-b:v", "1200k", "-maxrate", "1200k", "-bufsize", "2400k", "-qmin", "10", "-qmax", "42", 
     "-vf", "scale=-1:%s" % size, "-b:a", "128k", tmp_file] )
    
    return retcode, tmp_file
    
def thumbnail(input_file):
    
    tmp_file = "%s/%s.png" % (settings.TEMPORARY_DIR, uuid.uuid4())
    retcode = runProcess(["ffmpeg", "-y" ,"-i", input_file, "-vframes","1", "-an", tmp_file] )
    
    return int(retcode),  tmp_file

def metadata(input_file):
    
    try:
        p = subprocess.Popen(["ffmpeg", "-i", input_file], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    except Exception:
        return None
    
    date = None
    size = None
    while p.poll() is None:
        
        for line in (p.stderr.readlines() + p.stdout.readlines()):
            date_re = re.match(r'[ ]+creation_time[ ]+:(.*)', line)
            if date_re is not None:
                date = parser.parse(date_re.group(1).strip())
            
            size_re = re.match(r'.* ([0-9]+x[0-9]+)[, ]', line)
            if size_re is not None:
                size = size_re.group(1).strip().split('x')
            
    return {'date' : date, 'size' : size }