import pytest
import json
import sys
from pathlib import Path
from app import app
from .api_testcases import transcript_full, transcript_single_language, metadata

# add src to path for import
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
from src._errors import error_messages
sys.path.remove(str(parent_dir))

@pytest.mark.parametrize('url, expected', [
    (f'/v1/transcripts?id={transcript_full["videoId"]}', transcript_full),
    (f'/v1/transcripts?id={transcript_single_language["videoId"]}&lang={transcript_single_language["transcripts"][0]["languageCode"]}', transcript_single_language),
    (f'/v1/metadata?id={metadata["videoId"]}', metadata)
])

@pytest.mark.api
def test_api(url, expected):
    response = app.test_client().get(url)
    res = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert res == expected


@pytest.mark.parametrize('endpoints, expected_code, expected_message', [
    ('/v1/transcripts', 400, error_messages["noVideoId"]),
    ('/v1/transcripts?id=P6FORpg0KVo&type=badtype', 400, error_messages["invalidOutput"]),
    ('/v1/transcripts?id=P6FORpg0KVo&lang=zzz', 404, error_messages["noTranscriptFoundForLanguage"]),
    ('/v1/translations', 400, error_messages["noVideoId"]),
    ('/v1/translations?id=P6FORpg0KVo', 400, error_messages["noTargetLanguage"]),
    ('/v1/metadata', 400, error_messages["noVideoId"]),
])

@pytest.mark.exceptions
def test_exceptions(endpoints, expected_code, expected_message):
    response = app.test_client().get(endpoints)
    body = json.loads(response.data.decode('utf-8'))
    assert response.status_code == expected_code
    assert body["message"] == expected_message