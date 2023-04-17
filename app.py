from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from _resources import Transcript, TranslatedTranscript, TranscriptMetadata
from _errors import InvalidAPIUsage, TranscriptionError


# Instantiate the app
app = Flask(__name__)
CORS(app)
api = Api(app, prefix='/v1')

app.config['TRAP_HTTP_EXCEPTIONS']=True


# Register API resources
api.add_resource(Transcript, "/transcripts/")
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