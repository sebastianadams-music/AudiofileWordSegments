#!/usr/bin/env python3

import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
from os import path, listdir
from shutil import copyfile
from random import randint

for filename in listdir("segments_in"):

    AUDIO_FILE = f"segments_in/{filename}"
    # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
    # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:    
        audio = r.record(source)  # read the entire audio file
        

    # recognize speech using Whisper
    try:
        recog = r.recognize_whisper(audio, language="english")
        print("Sphinx thinks you said " + recog)
        rand = randint(100, 999)
        dest = f"segments_out/{recog}_{rand}.wav"
        copyfile(AUDIO_FILE, dest)

    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Whisper error; {0}".format(e))

