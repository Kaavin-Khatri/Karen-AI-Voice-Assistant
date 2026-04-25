import sounddevice as sd
import queue
import speech_recognition as sr

class SoundDeviceMicrophone(sr.AudioSource):
    def __init__(self, device=None, sample_rate=16000, chunk_size=1024):
        self.device = device
        self.SAMPLE_RATE = sample_rate
        self.CHUNK = chunk_size
        self.SAMPLE_WIDTH = 2  # 16-bit int (2 bytes)
        self.stream = None

    def __enter__(self):
        self.q = queue.Queue()
        
        def callback(indata, frames, time, status):
            self.q.put(bytes(indata))

        self.audio_stream = sd.RawInputStream(
            samplerate=self.SAMPLE_RATE,
            blocksize=self.CHUNK,
            device=self.device,
            channels=1,
            dtype='int16',
            callback=callback
        )
        self.audio_stream.start()
        self.stream = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.audio_stream.stop()
        self.audio_stream.close()
        self.stream = None
        self.audio_stream = None

    def read(self, size):
        # speech_recognition asks for 'size' frames. 
        # Our callback provides exactly self.CHUNK frames per item.
        # We assume size matches self.CHUNK for simplicity in this adapter.
        return self.q.get()
