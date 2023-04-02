# youtube-transcriber-api
 
Youtube's official API currently does not support fetching of a video's transcript. This API is built on [jdepoix's API](https://github.com/jdepoix/youtube-transcript-api), and provides a simple interface for retrieving pure-text transcripts for YouTube videos. It also provides the ability to translate transcripts into different languages.

The API is currently hosted on Vercel and it is available for anyone to use at no cost.

## API Endpoints

Note: All language codes used should follow the **[ISO 639-1](https://www.w3schools.com/tags/ref_language_codes.asp)** standard (case-sensitive)

### Transcripts

```
GET /1/transcripts/{{id}}
```

Retrieve transcripts for a specified YouTube video.
(try: https://youtube-transcriber-api.vercel.app/1/transcripts/?id=k_GM1JA608Y&lang=en)

**Query Parameters**

| Parameter            | Required | Note                                                                                                                                                                 |
|----------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `id`                 | Yes      | The ID of the YouTube video                                                                                                                                          |
| `lang`               | No       | The language code for the desired transcript. If no language is specified, all available transcripts will be returned                                                |
| `output_type`        | No       | The desired output format. Accepts `json`, `text`, `srt`, and `vtt`. Default to `text` if not specified                                                              |
| `include_line_break` | No       | Boolean (0 or 1) indicating whether the transcript should contain line breaks. Only applies for output_type `text`. Default to 0 if not specified                    |
| `include_sfx`        | No       | Boolean (0 or 1) indicating whether the transcript should contain sound effects information eg. \[Cheering\], \[Applause\], \[Music\]. Default to 0 if not specified |


**Response**

The request returns a JSON object containing the following fields:

| Field         | Description                                                                                                                                                                                                                                                                                                                                                                   |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `video_id`    | The ID of the YouTube video                                                                                                                                                                                                                                                                                                                                                   |
| `transcripts` | A list of transcripts. Each transcript has the following fields:<br><br>`language`: The language of the transcript<br>`languageCode`: The ISO 639-1 code<br>`isGenerated`: Boolean indicating whether the transcript is machine-generated <br>`isTranslatable`: Boolean indicating whether the transcript can be translated<br>`text`: The transcript in the specified format |


### Translation

```
GET /1/translations/{{id}}{{lang}}
```

Retrieve a translated transcript for a specified YouTube video.
(try: https://youtube-transcriber-api.vercel.app/1/transcripts/?id=k_GM1JA608Y&lang=es)

**Query Parameters**
| Parameter | Required | Note                                      |
|-----------|----------|-------------------------------------------|
| `id`      | Yes      | The ID of the YouTube video               |
| `lang`    | Yes      | The language code for the target language |

**Response**

The request returns a JSON object containing the following fields:

| Field            | Description                                 |
|------------------|---------------------------------------------|
| `video_id`       | The ID of the YouTube video                 |
| `sourceLanguage` | The language code of the source transcript  |
| `targetLanguage` | The language code of the target translation |
| `transcripts`    | The transcript text                         |


### Metadata

```
GET /1/metadata/{{id}}
```

Retrieve transcript metadata for a specified YouTube video.
(try: https://youtube-transcriber-api.vercel.app/1/metadata/?id=k_GM1JA608Y)

**Query Parameters**

| Parameter | Required | Note                        |
|-----------|----------|-----------------------------|
| `id`      | Yes      | The ID of the YouTube video |


**Response**

The request returns a JSON object containing the following fields:

| Field          | Description                                                                                                       |
|----------------|-------------------------------------------------------------------------------------------------------------------|
| `video_id`     | The ID of the YouTube video.                                                                                      |
| `transcripts`  | A list of transcript metadata. Each item has the following fields:<br><br>`language`: The language of the transcription<br>`languageCode`: The ISO 639-1 code<br>`isGenerated`: Boolean indicating whether the transcript is machine-generated <br>`isTranslatable`: Boolean indicating whether the transcript can be translated |


## Future Plans
This project is still in active development. Future plans include
- Add rate limiting
- Proper API documentation
- Automated testing
- Integration with Large Language Models like GPT-3 to improve transcript quality, and enable transcript summarisation and generative Q&A

## Donation
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/mjzhang)

## License
[See license](https://github.com/mongj/youtube-transcriber-api/blob/main/LICENSE)
