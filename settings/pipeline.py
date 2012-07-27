PIPELINE = True
PIPELINE_AUTO = False
PIPELINE_VERSION = True
PIPELINE_VERSIONING = 'pipeline.versioning.git.GitRevVersioning'
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None
PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'

PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'css/style.css',
        ),
        'output_filename': 'c/base.r?.css',
    },
}
PIPELINE_COMPILERS = (
    'pipeline.compilers.stylus.StylusCompiler',
)