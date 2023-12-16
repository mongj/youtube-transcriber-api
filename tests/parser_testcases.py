# testcases for parser
test_transcript = [
    {'text': 'hello world (applause) this is a test transcript', 'start': 1.000, 'duration': 3.999}, 
    {'text': '(applause)', 'start': 4.000, 'duration': 3.999},
    {'text': 'this is a test transcript', 'start': 7.000, 'duration': 3.999}
]

parsed_text = "hello world (applause) this is a test transcript\n(applause)\nthis is a test transcript"
parsed_srt = "1\n00:00:01,000 --> 00:00:04,000\nhello world (applause) this is a test transcript\n\n2\n00:00:04,000 --> 00:00:07,000\n(applause)\n\n3\n00:00:07,000 --> 00:00:10,999\nthis is a test transcript\n"
parsed_webvtt = "WEBVTT\n\n00:00:01.000 --> 00:00:04.000\nhello world (applause) this is a test transcript\n\n00:00:04.000 --> 00:00:07.000\n(applause)\n\n00:00:07.000 --> 00:00:10.999\nthis is a test transcript\n"
parsed_no_linebreak = "hello world (applause) this is a test transcript (applause) this is a test transcript"
parsed_no_sfx = "hello world this is a test transcript\n\nthis is a test transcript"