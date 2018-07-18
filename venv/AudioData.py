import numpy as np
from scipy.io import wavfile
import pyaudio
import wave
import datetime
import os

class AudioData:
    """
    Records audio and analyze it for sounds larger
    than the Treshold.
    """
    #minimum tolerable sound level.
    noise_treshold = 0
    #Flag for post recorded sound analysis.
    has_loud_noise = False
    #Audio Recording standard settings
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"
    #sound intensinty
    sound_file_max_ch1 = 0
    sound_file_max_ch2 = 0
    #audio array
    channel1 = np.zeros(0)
    channel2 = np.zeros(0)
    freq = 0

    def __init__(self,_noise_treshold):
        self.noise_treshold = _noise_treshold
        self.record_audio(self.FORMAT,self.CHANNELS,
                          self.RATE,self.CHUNK,
                          self.RECORD_SECONDS,self.WAVE_OUTPUT_FILENAME)

        self.read_audio_file(self.WAVE_OUTPUT_FILENAME)
        self.statistics()

    def display(self):
        print(self.freq)
        print("ch1:",self.channel1[:40])
        print("------------------")
        print("ch2",self.channel2[:40])

    def statistics(self):
        """
        checks max inputs of the sound.
        Decides to flag or not has_loud_sounds.
        :return:
        """
        self.sound_file_max_ch1 = np.max(self.channel1)
        self.sound_file_max_ch2 = np.max(self.channel2)

    def was_there_noise(self):
        if (self.sound_file_max_ch1 > self.noise_treshold) or (self.sound_file_max_ch2 > self.noise_treshold):
            self.has_loud_noise = True

    def clean_variables(self):
        self.channel1 = np.zeros(0)
        self.channel2 = np.zeros(0)
        self.freq = 0
        self.has_loud_noise = False

    def record_audio(self,format,channels, rate, chunk,
                     record_seconds, wave_output_filename):
        """
        captures from default microphone RECORD_SECONDS duration of audio and
        saves into WAVE_OUTPUT_FILENAME
        """
        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=format, channels=channels,
                            rate=rate, input=True,
                            frames_per_buffer=chunk)
        print("recording...")
        frames = []

        for i in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)
        print("finished recording")

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        wave_file = wave.open(wave_output_filename, 'wb')
        wave_file.setnchannels(channels)
        wave_file.setsampwidth(audio.get_sample_size(format))
        wave_file.setframerate(rate)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

    def read_audio_file(self,filename):
        """
            Reads filename. returns array of data.
        """
        print("Start analyzing file:", filename)
        fs, data = wavfile.read(filename)

        print("file read. stored in AudioData object")
        self.channel1 = data[:,0]
        self.channel2 = data[:,1]
        self.freq = fs

    def listen(self):
        """
        record, analyze and evaluate if noise was produced.
        returns file and flag.
        :return:
        """
        #timestamp
        timenow = datetime.datetime.utcnow()
        new_sound_file = "listen_" + timenow.strftime("%Y_%j_%H%M%S%f") + ".wav"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print ("dir_path:::",dir_path)
        self.record_audio(self.FORMAT,self.CHANNELS,self.RATE,self.CHUNK,self.RECORD_SECONDS,new_sound_file)
        self.read_audio_file(new_sound_file)
        self.statistics()
        self.was_there_noise()

        if (self.has_loud_noise):
            print("AudioData: Large sound detected (above treshold of {}).".format(self.noise_treshold))
            self.clean_variables()
            return new_sound_file
        else:
            self.clean_variables()
            os.remove(dir_path + "/" + new_sound_file)
            return None


