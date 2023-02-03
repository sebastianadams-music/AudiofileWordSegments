import whisper_timestamped as whisper
import ffmpeg
# pip3 install git+https://github.com/linto-ai/whisper-timestamped 
from pydub import AudioSegment

EXTEND_SEGS = 10 # extend all segments by x ms on front and
VIDEO_FILE = "warhol.mp4" # PUT VIDEO FILE HERE

song = AudioSegment.from_file(VIDEO_FILE, "mp4") # if source is other
song.export("temp.wav", format="wav") # have to create temp file for whisper
audio = whisper.load_audio("temp.wav")

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
    for worddata in words:
        word = worddata["text"]
        start_time = (worddata["start"])
        end_time = (worddata["end"]) + (EXTEND_SEGS/1000)
        confidence = worddata["confidence"]
        print(word, start_time, end_time, confidence)
        if confidence > 0.5:
            length =  end_time - start_time
            video = ffmpeg.input(VIDEO_FILE, ss=start_time, t=length)
            dest = f"segments_out/{word}_{counter}.mp4"
            stream = ffmpeg.output(video, dest)
            
            ffmpeg.run(stream)
            counter += 1
        

