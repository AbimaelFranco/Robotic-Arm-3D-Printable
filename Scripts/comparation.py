import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import freqz, correlate
import pyaudio
import wave

# The following code is used to compare audio files based on their dominant frequencies.
# It includes functions to play audio, calculate the dominant frequency, and compare frequencies with tolerance.

# Function to play audio
def play_audio(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to calculate the dominant frequency
def calculate_dominant_frequency(audio, fs):
    N = len(audio)
    fft_result = np.fft.fft(audio)
    fft_magnitude = np.abs(fft_result[:N // 2 + 1])
    frequencies = np.fft.fftfreq(N, d=1/fs)[:N // 2 + 1]
    dominant_frequency = frequencies[np.argmax(fft_magnitude)]
    return dominant_frequency

# Function to compare dominant frequencies with tolerance
def compare_frequencies(audio_ref, fs_ref, audio_comp, fs_comp, tolerance=3.0):
    dominant_frequency_ref = calculate_dominant_frequency(audio_ref, fs_ref)
    dominant_frequency_comp = calculate_dominant_frequency(audio_comp, fs_comp)
    
    if abs(dominant_frequency_ref - dominant_frequency_comp) <= tolerance:
        return True
    else:
        return False

# Audio files to compare
def comparison():
    audio_files = ['Audios/filteredAudio1.wav', 'Audios/filteredAudio2.wav', 'Audios/filteredAudio3.wav']
    reference_audio = '8.wav'  # Reference audio for comparison
    tolerance = 5.0  # Tolerance for frequency comparison (±3 Hz)
    result = " "

    # Load reference audio
    audio_ref, fs_ref = sf.read(reference_audio)

    # Compare each file with the reference audio and display results
    for file in audio_files:
        audio_comp, fs_comp = sf.read(file)
        
        if compare_frequencies(audio_ref, fs_ref, audio_comp, fs_comp, tolerance):
            result = file
        else:
            pass
       
        # Play the compared audio
        # print(f"Playing audio file: {file}")
        # play_audio(file)

    if result == 'filteredAudio1.wav':
        audio = "Audio1"
        return audio
    elif result == 'filteredAudio2.wav':
        audio = "Audio2"
        return audio
    elif result == 'filteredAudio3.wav':
        audio = "Audio3"
        return audio
    else:
        audio = "Audio not identified"
        return audio
