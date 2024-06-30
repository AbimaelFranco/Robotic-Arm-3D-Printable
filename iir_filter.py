import pyaudio
import numpy as np
import scipy.signal as signal
import soundfile as sf
import os

# The following code is used to record audio, apply a bandpass filter, and save the filtered audio to a file.

def record_audio():
    # Recording parameters
    fs = 100000  # Sampling frequency (Hz) increased for better quality
    nBits = 16  # Number of bits per sample
    nChannels = 1  # Number of channels (1 for mono)
    duration = 5  # Recording duration (seconds)

    # PyAudio configuration
    p = pyaudio.PyAudio()

    # Start recording
    print("Starting audio recording...")
    stream = p.open(format=pyaudio.paInt16, channels=nChannels, rate=fs, input=True, frames_per_buffer=1024)
    frames = []

    for i in range(0, int(fs / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording finished.")

    # Stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert data to a numpy array
    audioData = np.frombuffer(b''.join(frames), dtype=np.int16)

    if len(audioData) == 0:
        raise ValueError('No audio data captured. Check your microphone and recording permissions.')
    else:
        # print('Audio data captured successfully.')
        pass

    # Filter parameters
    fc = 1400  # Center frequency (Hz)
    bw = 200  # Bandwidth of the filter (Hz)
    order = 4  # Order of the filter

    # Calculate normalized cutoff frequencies
    f1 = (fc - bw / 2) / (fs / 2)  # Lower normalized cutoff frequency
    f2 = (fc + bw / 2) / (fs / 2)  # Upper normalized cutoff frequency

    # Ensure the frequencies are within the allowed range
    if not (0 < f1 < 1 and 0 < f2 < 1):
        raise ValueError(f'Cutoff frequencies must be between 0 and 1 after normalization. f1: {f1}, f2: {f2}')

    # Design the Butterworth bandpass filter
    b, a = signal.butter(order, [f1, f2], btype='band')

    # Apply the filter to the captured audio signal
    filteredAudio = signal.lfilter(b, a, audioData)

    # Normalize the filtered audio to avoid distortion
    filteredAudio = filteredAudio / np.max(np.abs(filteredAudio), axis=0)

    # Save the filtered audio
    filename = '8.wav'
    sf.write(filename, filteredAudio, fs)

    if os.path.exists(filename):
        pass
        # print(f'The filtered audio has been saved to {filename}')
    else:
        raise IOError('Error saving the audio file.')
