from werkzeug.exceptions import HTTPException
from youtube_transcript_api._errors import (
    FailedToCreateConsentCookie,
    NoTranscriptAvailable,
    NoTranscriptFound,
    NotTranslatable,
    TooManyRequests,
    TranscriptsDisabled,
    TranslationLanguageNotAvailable,
    VideoUnavailable,
    YouTubeRequestFailed,
)


YOUTUBE_API_ERRORS = (
    FailedToCreateConsentCookie,
    NoTranscriptAvailable,
    NoTranscriptFound,
    NotTranslatable,
    TooManyRequests,
    TranscriptsDisabled,
    TranslationLanguageNotAvailable,
    VideoUnavailable,
    YouTubeRequestFailed,
)


class CustomHTTPException(HTTPException):
    """
    Base class for custom HTTP exception
    """
    def __init__(self, description):
        super().__init__()
        self.description = description
        

class InvalidAPIUsage(CustomHTTPException):
    code=400


class TranscriptionError(CustomHTTPException):
    code=500