import tempfile
import subprocess
import re

def runProcess(exe):    
    retcode = subprocess.check_call(exe)
    return retcode

def webm(input_file):
    
    tmp_file = "%s.webm" % tempfile.mkstemp()[1]
    
    retcode = runProcess(["ffmpeg", "-y" ,"-i", input_file,  tmp_file] )
    
    return retcode, tmp_file
    
def thumbnail(input_file):
    
    tmp_file = "%s.png" % tempfile.mkstemp()[1]
    
    retcode = runProcess(["ffmpeg", "-y" ,"-i", input_file, "-vframes","1","-ss", "2", "-an", tmp_file] )
    
    
    return int(retcode),  tmp_file

def metadata(input_file):
    
    p = subprocess.Popen(["ffmpeg", "-i", input_file], stderr=subprocess.PIPE)

    while p.poll() is None:
        
        for line in p.stderr.readlines():
            test = re.match('creation_time[]+:(.*)')
            if test is not None:
                date = test.group(1).strip()
                break
            
    print date