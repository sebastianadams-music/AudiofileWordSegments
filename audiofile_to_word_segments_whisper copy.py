import whisper_timestamped as whisper
# pip3 install git+https://github.com/linto-ai/whisper-timestamped 
from pydub import AudioSegment

EXTEND_SEGS = 10 # extend all segments by x ms on front and

AUDIO_FILE = "how-blurs-filters-work-computerphile_1.mp4" # PUT AUDIO FILE HERE

audio = whisper.load_audio(AUDIO_FILE)
song = AudioSegment.from_wav(AUDIO_FILE) # if source is WAV
song = AudioSegment.from_file(AUDIO_FILE, "mp4") # if source is other
# song = AudioSegment.from_mp3(AUDIO_FILE) # if source is MP3

model = whisper.load_model("tiny", device="cpu")

result = whisper.transcribe(model, audio, language="en")

import json
y = json.dumps(result, indent = 2, ensure_ascii = False)
# print(y)
dict = json.loads(y)
# print(dict["segments"])
counter = 0
for segment in dict["segments"]:
    words = segment["words"]
    # print("words", words)
    for worddata in words:
        # print(word)
        word = worddata["text"]
        # print(word)
        start_time = (worddata["start"] * 1000)
        end_time = (worddata["end"] * 1000) + EXTEND_SEGS
        confidence = worddata["confidence"]
        print(word, start_time, end_time, confidence)
        if confidence > 0.5:
            split_audio = song[start_time:end_time]
            faded = split_audio.fade_in(5).fade_out(5)
            dest = f"segments_out/{word}_{counter}.wav"
            faded.export(dest, format="wav")
            counter += 1
        

