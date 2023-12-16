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

error_messages = {
    "noVideoId": "video id is required but not provided",
    "invalidOutput": "Invalid output type. Output type must be either 'json','text','srt', or 'vtt'",
    "noTranscriptFoundForLanguage": "No transcript is found for the specified language",
    "noTargetLanguage": "target language is required but not provided"
}

class CustomHTTPException(HTTPException):
    """
    Base class for custom HTTP exception
    """
    def __init__(self, description):
        super().__init__()
        self.description = description
        

class InvalidAPIUsage(CustomHTTPException):
    """
    Custom HTTP exception for invalid client request eg. query parameter not provided
    """
    code=400


class TranscriptionError(CustomHTTPException):
    """
    Custom HTTP exception for error encountered during transcription eg. video cannot be found
    """
    code=200