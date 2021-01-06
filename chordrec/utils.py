import os
import os.path
import tempfile

from chord_recognition.utils import read_audio
from chord_recognition.predict import ChordRecognition, UnsupportedSampleRate
from pydub import AudioSegment
import soundfile as sf


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def ann_to_dict(annotations, skip_nonchord=True, nonchord='N'):
    result = []
    for row in annotations:
        start, end, note = row
        if skip_nonchord and note == nonchord:
            continue
        new_ann = {
            "start": start,
            "end": end,
            "attributes": {"label": note},
            "data": {"note": note}
        }
        result.append(new_ann)
    return result


def read_audio_from_stream(stream, sr=None, mono=False, duration=None, exp_format="wav"):
    """Reads an audio file from stream.
    Since librosa does not support reading mp3 in buffer.
    https://github.com/librosa/librosa/pull/1066 because of
    https://github.com/libsndfile/libsndfile/pull/499
    """
    _, file_ext = stream.filename.rsplit('.', 1)
    ext_converter = {
        'mp3': AudioSegment.from_mp3,
    }
    converter = ext_converter.get(file_ext)
    if not converter:
        raise InvalidUsage(f"Invalid extension: {file_ext}")

    with tempfile.NamedTemporaryFile() as ntf:
        sound = converter(stream)
        sound.export(ntf, format=exp_format)
        return read_audio(ntf.name, sr, mono, duration)


def process_audio(audio, duration):
    audio_waveform, sr, = read_audio_from_stream(audio, mono=True, duration=duration)
    recognition = ChordRecognition(nonchord=True)
    try:
        ann = recognition.process(
            audio_waveform=audio_waveform,
            sr=sr)
    except UnsupportedSampleRate as e:
        raise InvalidUsage(str(e))
    ann_dict = ann_to_dict(ann)
    return ann_dict, audio_waveform, sr


def save_file(file_path, data, sample_rate):
    saved_path = file_path.replace('.mp3', '.wav')
    dir_path = os.path.dirname(saved_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    sf.write(saved_path, data, sample_rate)
    return saved_path
