import io
import wave
import contextlib

import pyaudio
import speech_recognition as sr

from .components import ComponentBase


class SpeechRecognition(ComponentBase):
    
    chunk = 1024
    channels = 1
    rate = 16000
    format = pyaudio.paInt16

    r = sr.Recognizer()
    m = sr.Microphone()
    p = pyaudio.PyAudio()

    def __init__(self, act_as_server=False, act_as_own=False, port=5000, host='localhost'):
        self.is_server = act_as_server
        self.is_own = act_as_own

    def start_listening(self):
        while(True):
            try:
                with self.m as source:
                    print("adjusting for ambient noise...")
                    self.r.adjust_for_ambient_noise(source, duration=0.5)
                    print("listening...")
                    audio = self.r.listen(source)

                    print(self.r.recognize_google(audio))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return None
            except Exception as e:
                print(e)
                return None

    def wave2text(self, wave_frames):
        try:
            container = io.BytesIO()

            wf = wave.open(container, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(wave_frames)

            container.seek(0)
            with sr.AudioFile(container) as source:
                audio = self.r.record(source)

            return self.r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None
        except Exception as e:
            print(e)
            return None
        


