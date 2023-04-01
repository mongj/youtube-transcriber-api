# youtube-transcriber-api
 
This API provides a simple interface for retrieving transcripts and metadata for YouTube videos. It also provides the ability to translate transcripts into different languages.

### API Endpoints

GET /transcripts/
Retrieve transcripts for a specified YouTube video.
(try: https://youtube-transcriber-api.vercel.app/transcripts/?id=k_GM1JA608Y&lang=en)

**Request Parameters**
id (required): The ID of the YouTube video.
lang: (optional) The language code for the desired transcript. If no language is specified, all available transcripts will be returned.

**Response**
The request returns a JSON object containing the following fields:
video_id: The ID of the YouTube video.
transcripts: An array of transcript objects. Each transcript object has the following fields:
language: The name of the language.
languageCode: The language code.
isGenerated: Boolean indicating whether the transcript is machine-generated.
isTranslatable: Boolean indicating whether the transcript can be translated.
text: The text of the transcript.

GET /metadata/
Retrieve metadata for a specified YouTube video.
(try: https://youtube-transcriber-api.vercel.app/metadata/?id=k_GM1JA608Y&lang=en)

**Request Parameters**
id (required): The ID of the YouTube video.

**Response**
The request returns a JSON object containing the following fields:
video_id: The ID of the YouTube video.
transcripts: An array of transcript objects. Each transcript object has the following fields:
language: The name of the language.
languageCode: The language code.
isGenerated: Boolean indicating whether the transcript is machine-generated.
isTranslatable: Boolean indicating whether the transcript can be translated.

GET /translations/
Retrieve a translated transcript for a specified YouTube video.
(try: https://youtube-transcriber-api.vercel.app/transcripts/?id=k_GM1JA608Y&lang=es)

**Request Parameters**
id (required): The ID of the YouTube video.
lang (required): The language code for the desired translation.

**Response**
The request returns a JSON object containing the following fields:
video_id: The ID of the YouTube video.
sourceLanguage: The language code of the source transcript.
targetLanguage: The language code of the target translation.
transcripts: The text of the translated transcript.