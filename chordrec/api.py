import logging
import os.path

from flask import Blueprint, send_from_directory, jsonify, current_app
from flask_cors import cross_origin
from webargs.flaskparser import use_args

from .fields import annotation_args
from .utils import process_audio, save_file
from .telegram import telegram_api


bp_api = Blueprint("api", __name__, url_prefix="/api/v1")
bpu = Blueprint("uploads", __name__, url_prefix="/uploads")
DEFAULT_AUDIO_DURATION = 60  # in seconds
FILE_STORAGE_PATH = '/tmp/uploads/'

logger = logging.getLogger(__name__)


@bp_api.route('/annotations/', methods=['POST'])
@use_args(annotation_args, location="files")
def annotations(args):
    file = args['file']
    logger.info('Uploaded %s' % file.filename)
    ann_dict, audio_waveform, Fs = process_audio(file, DEFAULT_AUDIO_DURATION)
    file.seek(0)
    if not current_app.config['DEBUG']:
        telegram_api.send_audio(file)
    file_path = os.path.join(FILE_STORAGE_PATH, file.filename)
    file_path = save_file(file_path, audio_waveform, Fs)
    logger.info('Saved %s' % file_path)
    # ToDo: compute audiowaveform peaks on BE side
    result = {
        'annotations': ann_dict,
    }
    return jsonify(result)


@bpu.route('/<filename>')
@cross_origin(allow_headers=['Content-Type'])
def uploads(filename):
    """For development purpose.
    nginx is used on production
    """
    return send_from_directory(FILE_STORAGE_PATH, filename)
