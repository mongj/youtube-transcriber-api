import sys
from pathlib import Path
from .parser_testcases import test_transcript, parsed_text, parsed_srt, parsed_webvtt, parsed_no_linebreak, parsed_no_sfx

# add src to path for import
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
from src import _parser
sys.path.remove(str(parent_dir))

def test_parse_text():
    assert _parser.parse_transcript(test_transcript, "text", True, True) == parsed_text

def test_parse_json():
    assert _parser.parse_transcript(test_transcript, "json", True, True) == test_transcript

def test_parse_srt():
    assert _parser.parse_transcript(test_transcript, "srt", True, True) == parsed_srt

def test_parse_webvtt():
    assert _parser.parse_transcript(test_transcript, "webvtt", True, True) == parsed_webvtt

def test_parse_no_linebreak():
    assert _parser.parse_transcript(test_transcript, "text", False, True) == parsed_no_linebreak

def test_parse_no_sfx():
    assert _parser.parse_transcript(test_transcript, "text", True, False) == parsed_no_sfx
