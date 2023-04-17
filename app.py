from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from youtube_transcript_api._errors import NoTranscriptFound

from _errors import InvalidAPIUsage, TranscriptionError
from _errors import YOUTUBE_API_ERRORS
from _settings import LANGUAGE_CODES, TRANSCRIPT_OUTPUT_TYPES
from _parser import parse_transcript
from _transcript import retrieve_transcript, build_transcript

# Instantiate the app
app = Flask(__name__)
CORS(app)
api = Api(app, prefix='/v1')

app.config['TRAP_HTTP_EXCEPTIONS']=True

class GeneratedTranscript(Resource):
    def get(self):
        # Get query params
        video_id = request.args.get('id')
        language_codes = request.args.get('lang')
        output_type = request.args.get('type') or "text"
        include_line_break = bool(int(request.args.get('lb') or 0))
        include_sfx = bool(int(request.args.get('sfx') or 0))

        # Validate request
        if not video_id:
            raise InvalidAPIUsage("video id is required but not provided")

        output_type = output_type.lower()
        if not output_type in TRANSCRIPT_OUTPUT_TYPES:
            raise InvalidAPIUsage("Invalid output type. Output type must be either 'json','text','srt', or 'vtt'")

        # Attempt to retrieve the transcript
        transcript_list = retrieve_transcript(video_id)

        # Retrieve the transcript in specified language. If no language was specified, all available transcripts will be returned
        if not language_codes:
            return {
                "video_id": video_id,
                "transcripts": [build_transcript(transcript, output_type, include_line_break, include_sfx) for transcript in transcript_list]
            }, 200
        else:
            try:
                transcript = transcript_list.find_transcript([language_codes])
                return {
                    "video_id": video_id,
                    "transcripts": [build_transcript(transcript, output_type, include_line_break, include_sfx)]
                }, 200
            except NoTranscriptFound:
                raise TranscriptionError("No transcript is found for the specified language")


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