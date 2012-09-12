from common import *
from pipeline import *
from subprocess import check_output
 
DEBUG = True

DISABLE_ROBOTS=True

PIPELINE_AUTO = True
PIPELINE_VERSION = False
PIPELINE_VERSIONING = 'pipeline.versioning.mtime.MTimeVersioning'

PIPELINE_STYLUS_BINARY = check_output(['which','stylus'])

INTERNAL_IPS = ('127.0.0.1')

