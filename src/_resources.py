from flask import request
from flask_restful import Resource

from youtube_transcript_api._errors import NoTranscriptFound

from ._errors import InvalidAPIUsage, TranscriptionError
from ._errors import YOUTUBE_API_ERRORS, error_messages
from ._settings import LANGUAGE_CODES, TRANSCRIPT_OUTPUT_TYPES
from ._parser import parse_transcript
from ._transcript import retrieve_transcript, build_transcript


class Transcript(Resource):
    def get(self):
        # Get query params
        video_id = request.args.get('id')
        language_codes = request.args.get('lang')
        output_type = request.args.get('type') or "text"
        include_line_break = bool(int(request.args.get('lb') or 0))
        include_sfx = bool(int(request.args.get('sfx') or 0))

        # Validate request
        if not video_id:
            raise InvalidAPIUsage(error_messages["noVideoId"])

        output_type = output_type.lower()
        if not output_type in TRANSCRIPT_OUTPUT_TYPES:
            raise InvalidAPIUsage(error_messages["invalidOutput"])

        # Attempt to retrieve the transcript
        transcript_list = retrieve_transcript(video_id)

        # Retrieve the transcript in specified language. If no language was specified, all available transcripts will be returned
        if not language_codes:
            return {
                "videoId": video_id,
                "transcripts": [build_transcript(transcript, output_type, include_line_break, include_sfx) for transcript in transcript_list]
            }, 200
        else:
            try:
                transcript = transcript_list.find_transcript([language_codes])
                return {
                    "videoId": video_id,
                    "transcripts": [build_transcript(transcript, output_type, include_line_break, include_sfx)]
                }, 200
            except NoTranscriptFound:
                raise TranscriptionError(error_messages["noTranscriptFoundForLanguage"])


class TranslatedTranscript(Resource):
    def get(self):
        # Get query params
        video_id = request.args.get('id')
        language_code = request.args.get('lang')

        # Validate request
        if not video_id:
            raise InvalidAPIUsage(error_messages["noVideoId"])
        if not language_code:
            raise InvalidAPIUsage(error_messages["noTargetLanguage"])

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
            raise InvalidAPIUsage(error_messages["noVideoId"])

        # Attempt to retrieve the transcript
        transcript_list = retrieve_transcript(video_id)

        return {
            "videoId": video_id,
            "transcripts": [
                {
                    "language": transcript.language,
                    "languageCode": transcript.language_code,
                    "isGenerated": transcript.is_generated,
                    "isTranslatable": transcript.is_translatable
                } for transcript in transcript_list
            ]
        }, 200
