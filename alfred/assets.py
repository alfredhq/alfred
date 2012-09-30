from flask_gears import Gears
from gears_clean_css import CleanCSSCompressor
from gears_uglifyjs import UglifyJSCompressor


gears = Gears(
    compressors={
        'text/css': CleanCSSCompressor.as_handler(),
        'application/javascript': UglifyJSCompressor.as_handler(),
    },
    extra_public_assets=(
        r'^js/jquery.*\.js$',
    ),
)
