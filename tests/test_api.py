import io
import re

import pytest
import responses


@responses.activate
def test_create_annotations(client, assert_value):
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
