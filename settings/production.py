from common import *
from pipeline import *
from subprocess import Popen, PIPE

 
DEBUG = True

DISABLE_ROBOTS=True

PIPELINE_AUTO = True
PIPELINE_VERSION = False
PIPELINE_VERSIONING = 'pipeline.versioning.mtime.MTimeVersioning'

PIPELINE_STYLUS_BINARY = Popen("which stylus", shell=True, stdout=PIPE).stdout.read().split('\n')[0]

INTERNAL_IPS = ('127.0.0.1')

