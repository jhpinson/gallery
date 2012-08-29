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
            'css/bootstrap.css',
            'css/style.css',
            'css/gallery.styl'
        ),
        'output_filename': 'c/base.r?.css',
    },
}

PIPELINE_JS = {
    'lazy': {
        'source_filenames': (
            #'js/Placeholders.min.js',
            'js/bootstrap.js',
            
        ),
        'output_filename': 'c/lazy.r?.js',
    },
}

PIPELINE_COMPILERS = (
    'pipeline.compilers.stylus.StylusCompiler',
)