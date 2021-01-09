import io
import re

import pytest
import responses


@responses.activate
def test_create_ann_success(client, assert_value):
    responses.add(
        'POST',
        re.compile(r'https://api.telegram.org/bot'),
        json={'ok': True})
    with open('tests/fixtures/let_it_be.mp3', 'rb') as f:
        data = {
            'file': (io.BytesIO(f.read()), 'let_it_be.mp3')
        }
    resp = client.post('/api/v1/annotations/',
                       data=data,
                       content_type='multipart/form-data')
    resp_data = resp.get_json()
    assert_value(resp_data, "create_annotations")


@responses.activate
def test_create_ann_invalid_format(client, assert_value):
    responses.add(
        'POST',
        re.compile(r'https://api.telegram.org/bot'),
        json={'ok': True})
    with open('tests/fixtures/simple_piano.wav', 'rb') as f:
        data = {
            'file': (io.BytesIO(f.read()), 'simple_piano.wav')
        }
    resp = client.post('/api/v1/annotations/',
                       data=data,
                       content_type='multipart/form-data')
    resp_data = resp.get_json()
    assert resp_data == {'files': {'file': ['Unsupported file format']}}


@responses.activate
def test_create_ann_invalid_sample_rate(client, assert_value):
    responses.add(
        'POST',
        re.compile(r'https://api.telegram.org/bot'),
        json={'ok': True})
    with open('tests/fixtures/let_it_be_16k.mp3', 'rb') as f:
        data = {
            'file': (io.BytesIO(f.read()), 'let_it_be_16k.mp3')
        }
    resp = client.post('/api/v1/annotations/',
                       data=data,
                       content_type='multipart/form-data')
    resp_data = resp.get_json()
    assert resp_data == {'message': 'Sample rate: 16000 is not supported'}
    assert resp.status_code == 422
