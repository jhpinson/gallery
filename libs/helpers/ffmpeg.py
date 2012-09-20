import tempfile
import subprocess

def runProcess(exe):    
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdtout = []
    stderr = []
    retcode = None
    while(True):
        retcode = p.poll() #returns None while subprocess is running
        stdtout.append(p.stdout.readline())
        stderr.append(p.stderr.readline())
      
        if(retcode is not None):
            break
    
    return retcode, stdtout, stderr

def webm(input_file):
    
    tmp_file = "%s.webm" % tempfile.mkstemp()[1]
    
    retcode, stdtout, stderr = runProcess(["ffmpeg", "-y" ,"-i", input_file,  tmp_file] )
    
    return retcode, stdtout, stderr, tmp_file
    
def thumbnail(input_file):
    
    tmp_file = "%s.png" % tempfile.mkstemp()[1]
    
    retcode, stdtout, stderr = runProcess(["ffmpeg", "-y" ,"-i", input_file, "-vframes","1","-ss", "2", "-an", tmp_file] )
    
    
    return retcode, stdtout, stderr, tmp_file