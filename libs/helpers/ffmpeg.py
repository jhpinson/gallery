import tempfile
import subprocess
import re
from dateutil import parser
import uuid
from django.conf import settings

def runProcess(exe):    
    retcode = subprocess.check_call(exe)
    return retcode

def webm(input_file):
    
    tmp_file = "%s.webm" % tempfile.mkstemp()[1]
    
    retcode = runProcess(["ffmpeg", "-y" ,"-i", input_file,  tmp_file] )
    
    return retcode, tmp_file
    
def thumbnail(input_file):
    
    tmp_file = "%s/%s.png" % (settings.TEMPORARY_DIR, uuid.uuid4())
    retcode = runProcess(["ffmpeg", "-y" ,"-i", input_file, "-vframes","1","-ss", "2", "-an", tmp_file] )
    
    return int(retcode),  tmp_file

def metadata(input_file):
    
    try:
        p = subprocess.Popen(["ffmpeg", "-i", input_file], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    except Exception:
        return None
    date = None
    while p.poll() is None:
        
        for line in (p.stderr.readlines() + p.stdout.readlines()):
            print line
            test = re.match(r'[ ]+creation_time[ ]+:(.*)', line)
            if test is not None:
                date = parser.parse(test.group(1).strip())
                break
            
    return date