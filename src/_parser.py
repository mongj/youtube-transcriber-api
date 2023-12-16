import re

from typing import Optional
from youtube_transcript_api.formatters import *

from ._settings import TRANSCRIPT_OUTPUT_TYPES


def parse_transcript(
        transcript: dict,
        output_type: str = "text",
        include_line_break: Optional[bool] = False,
        include_sfx: Optional[bool] = False
):
    """
    parse_transcript parses a transcript and return it in the specified format

    :param `transcript`: a dictionary object returned by transcript.fetch()
    :param `formatter`: transcript can be formatted as `text`, `json`, `srt`, or `webvtt`.
    :param `include_line_break`: boolean to indicate if transcript should contain line breaks. This only applies if formatter=`text`.
    :param `include_sfx`: boolean to indicate if transcript should contain sound effects information eg. [Music], [Cheering].
    :return: returns a parsed transcript in the specified format (JSON for `JSON` and string for the rest)
    """

    formatter = TRANSCRIPT_OUTPUT_TYPES[output_type]
    parsed_transcript = formatter.format_transcript(transcript)

    if not include_sfx:
        parsed_transcript = re.sub(r"\([^\)]*\)", "", parsed_transcript)
        parsed_transcript = re.sub(r"(?![\n])\s{2,}", " ", parsed_transcript)

    if (not include_line_break) and (output_type == "text"):
        parsed_transcript = parsed_transcript.replace(
            "\n", " ").replace("  ", "\n")

    if output_type == "json":
        parsed_transcript = json.loads(parsed_transcript)

    return parsed_transcript
