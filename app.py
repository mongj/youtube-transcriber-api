import re

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from werkzeug.exceptions import HTTPException

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._transcripts import TranscriptList
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

from _errors import InvalidAPIUsage, TranscriptionError
from _settings import LANGUAGE_CODES

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

# Instantiate the app
app = Flask(__name__)
api = Api(app)

app.config['TRAP_HTTP_EXCEPTIONS']=True

class GeneratedTranscript(Resource):
    def get(self):
        # Get query params
        video_id = request.args.get('id')
        language_codes = request.args.get('lang')

        # Validate request
        if not video_id:
            raise InvalidAPIUsage("video id is required but not provided")
        
        # Attempt to retrieve the transcript
        transcript_list = retrieve_transcript(video_id)

        # Retrieve the transcript in specified language. If no language was specified, all available transcripts will be returned
        if not language_codes:
            return {
                "video_id": video_id,
                "transcripts": [
                    {
                        "language": transcript.language,
                        "languageCode": transcript.language_code,
                        "isGenerated": transcript.is_generated,
                        "isTranslatable": transcript.is_translatable,
                        "transcript": parse_transcript(transcript.fetch())
                    } for transcript in transcript_list
                ]
            }, 200
        else:
            try:
                transcript = transcript_list.find_transcript([language_codes])
                return {
                    "video_id": video_id,
                    "transcripts": [
                        {
                            "language": transcript.language,
                            "languageCode": transcript.language_code,
                            "isGenerated": transcript.is_generated,
                            "isTranslatable": transcript.is_translatable,
                            "transcript": parse_transcript(transcript.fetch())
                        }
                    ]
                }, 200
            except NoTranscriptFound as e:
                raise TranscriptionError("No transcript is found for the specified language")


class TranscriptMetadata(Resource):
    def get(self):
        # Get query params
        video_id = request.args.get('id')

        # Validate request
        if not video_id:
            raise InvalidAPIUsage("video id is required but not provided")
        
        # Attempt to retrieve the transcript
        transcript_list = retrieve_transcript(video_id)

        return {
            "video_id": video_id,
            "transcripts": [
                {
                    "language": transcript.language,
                    "languageCode": transcript.language_code,
                    "isGenerated": transcript.is_generated,
                    "isTranslatable": transcript.is_translatable
                } for transcript in transcript_list
            ]
        }, 200
    
# TO-DO
class TranslatedTranscript(Resource):
    def get(self):
        # Get query params
        video_id = request.args.get('id')
        language_code = request.args.get('lang')

        # Validate request
        if not video_id:
            raise InvalidAPIUsage("video id is required but not provided")
        if not language_code:
            raise InvalidAPIUsage("target language is required but not provided")
        
        # Attempt to retrieve the transcript
        transcript_list = retrieve_transcript(video_id)

        # Translate transcript
        transcript = transcript_list.find_transcript(LANGUAGE_CODES)
        try:
            translated_transcript = transcript.translate(language_code)
        except YOUTUBE_API_ERRORS as e:
            raise TranscriptionError(e.cause)

        return {
            "videoId": video_id,
            "sourceLanguage": transcript.language_code,
            "targetLanguage": language_code,
            "transcripts": parse_transcript(translated_transcript.fetch())
        }, 200

# Parse transcript object into string
def parse_transcript(transcript) -> str:
    parsed_transcript = ""

    for text in transcript:
        t = text["text"]
        parsed_transcript += t + " "
    
    parsed_transcript = parsed_transcript.replace('>>','')
    parsed_transcript = re.sub("[\[].*?[\]]", '', parsed_transcript)
    parsed_transcript = parsed_transcript.strip()

    return parsed_transcript

def retrieve_transcript(video_id) -> TranscriptList:
    try:
        return YouTubeTranscriptApi.list_transcripts(video_id)
    except YOUTUBE_API_ERRORS as e:
        raise TranscriptionError(e.cause)


# Register API resources
api.add_resource(GeneratedTranscript, "/transcripts/")
api.add_resource(TranscriptMetadata, "/metadata/")
api.add_resource(TranslatedTranscript, "/translations/")


# Register custom error handlers
app.register_error_handler(InvalidAPIUsage, InvalidAPIUsage)
app.register_error_handler(TranscriptionError, TranscriptionError)


# Return JSON instead of HTML for HTTP errors.
@app.errorhandler(HTTPException)
@app.errorhandler(InvalidAPIUsage)
@app.errorhandler(TranscriptionError)
def handle_exception(e):
    return jsonify(message=e.description), e.code


if __name__ == '__main__':
    app.run(debug=False)