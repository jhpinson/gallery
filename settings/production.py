from common import *
from pipeline import *
from subprocess import check_output
 
DEBUG = False
PIPELINE_AUTO = True
PIPELINE_VERSION = False
PIPELINE_VERSIONING = 'pipeline.versioning.mtime.MTimeVersioning'

PIPELINE_STYLUS_BINARY = check_output(['which','stylus'])


TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

INSTALLED_APPS += (
    'raven.contrib.django',
)

if SENTRY_SITE is None:
    raise Exception('You must define common.SENTRY_SITE')

if SENTRY_DSN is None:
    raise Exception('You must define common.SENTRY_DSN')
