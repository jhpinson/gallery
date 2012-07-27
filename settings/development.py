from common import *
from pipeline import *
from subprocess import check_output
 
DEBUG = True

DISABLE_ROBOTS=True

PIPELINE_AUTO = True
PIPELINE_VERSION = False
PIPELINE_VERSIONING = 'pipeline.versioning.mtime.MTimeVersioning'

PIPELINE_STYLUS_BINARY = check_output(['which','stylus'])

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INTERNAL_IPS = ('127.0.0.1')

INSTALLED_APPS += (
    'devserver',
    'resetdb',
    'debug_toolbar',
)

DEVSERVER_MODULES = (
    #'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',

)
DEVSERVER_TRUNCATE_SQL = False