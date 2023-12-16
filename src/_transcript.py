from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._transcripts import TranscriptList

from ._parser import parse_transcript
from ._errors import YOUTUBE_API_ERRORS
from ._errors import TranscriptionError

# Retrieve transcript as a TranscriptList object
def retrieve_transcript(video_id) -> TranscriptList:
    try:
        return YouTubeTranscriptApi.list_transcripts(video_id)
    except YOUTUBE_API_ERRORS as e:
        raise TranscriptionError(e.cause)


# Build a transcript as a Python dictionary
def build_transcript(transcript, output_type, include_line_break, include_sfx):
    return {
        "language": transcript.language,
        "languageCode": transcript.language_code,
        "isGenerated": transcript.is_generated,
        "isTranslatable": transcript.is_translatable,
        "text": parse_transcript(transcript.fetch(), output_type, include_line_break, include_sfx)
    }
