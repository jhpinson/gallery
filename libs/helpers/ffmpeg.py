import tempfile
import subprocess

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