import os
import os.path
import tempfile

from chord_recognition.utils import read_audio
from chord_recognition.predict import annotate_audio
from pydub import AudioSegment
import soundfile as sf


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


def read_audio_from_stream(stream, Fs=None, mono=False, duration=None, exp_format="wav"):
    """Reads an audio file from stream.
    Since librosa does not support reading mp3 in buffer.
    https://github.com/librosa/librosa/pull/1066 because of
    https://github.com/libsndfile/libsndfile/pull/499
    """
    _, file_ext = stream.filename.rsplit('.', 1)
    ext_converter = {
        'mp3': AudioSegment.from_mp3,
        'wav': AudioSegment.from_wav,
    }
    converter = ext_converter.get(file_ext)
    if not converter:
        raise ValueError(f"Invalid extension: {file_ext}")

    with tempfile.NamedTemporaryFile() as ntf:
        sound = converter(stream)
        sound.export(ntf, format=exp_format)
        return read_audio(ntf.name, Fs, mono, duration)


def process_audio(audio, duration):
    audio_waveform, Fs, = read_audio_from_stream(audio, mono=True, duration=duration)
    ann = annotate_audio(audio_waveform, Fs, nonchord=True)
    ann_dict = ann_to_dict(ann)
    return ann_dict, audio_waveform, Fs


def save_file(file_path, data, sample_rate):
    saved_path = file_path.replace('.mp3', '.wav')
    dir_path = os.path.dirname(saved_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    sf.write(saved_path, data, sample_rate)
    return saved_path
