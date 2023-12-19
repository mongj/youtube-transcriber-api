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


class InvalidAPIUsage(HTTPException):
    """
    Custom HTTP exception for invalid client request eg. query parameter not provided
    """
    def __init__(self, description):
        self.description = description
        self.code=400


class TranscriptionError(HTTPException):
    """
    Custom HTTP exception for error encountered during transcription eg. video cannot be found
    """
    def __init__(self, description):
        self.description = description

        if description ==  FailedToCreateConsentCookie.cause:
            self.code=400
        elif description ==  NoTranscriptAvailable.cause:
            self.code=404
        elif description ==  NoTranscriptFound.cause:
            self.code=404
        elif description ==  NotTranslatable.cause:
            self.code=404
        elif description ==  TooManyRequests.cause:
            self.code=403
        elif description ==  TranscriptsDisabled.cause:
            self.code=404
        elif description ==  TranslationLanguageNotAvailable.cause:
            self.code=404
        elif description ==  VideoUnavailable.cause:
            self.code=404
        elif description ==  YouTubeRequestFailed.cause:
            self.code=400
        elif description == error_messages["noTranscriptFoundForLanguage"]:
            self.code=404
        else:
            self.code=500