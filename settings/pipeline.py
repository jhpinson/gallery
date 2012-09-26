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
            'css/jquery.jgrowl.css',
            'video-js/video-js.css',
            'css/galleries.styl',
            'css/ox-gallery.css',
            'css/gallery.styl',
        
        ),
        'output_filename': 'c/base.r?.css',
    },
}

PIPELINE_JS = {
    'lazy': {
        'source_filenames': (
            'js/libs/jquery.ba-serializeobject.js',
            'js/libs/jquery.dajax.core.js',
            'dajaxice/dajaxice.core.js',
            'js/libs/jquery.easing.1.3.js',
            'js/libs/jquery.ui.widget.js',
            'js/libs/fileupload/jquery.iframe-transport.js',
            'js/libs/fileupload/jquery.fileupload.js',
            'js/libs/jquery.jgrowl.js',
            'video-js/video.js',
            'js/bootstrap.js',
            'js/thumbnails.js',
            'js/html-id.js',
            'js/dajaxice.forms-helpers.js',
            'js/lazy-modal.js',
            'js/lazy-fileupload.js',
            'js/libs/jquery.ox-gallery.js',
            'js/messages.js',
            'js/lazy-gallery.js',
            'js/lazy-video.js',
            
        ),
        'output_filename': 'c/lazy.r?.js',
    },
}

PIPELINE_COMPILERS = (
    'pipeline.compilers.stylus.StylusCompiler',
)