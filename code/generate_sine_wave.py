import numpy as np
import scipy.io.wavfile as wavfile

def generate_and_write(sample_rate, duration_sec, frequencies, amplitudes=None, add_noise=False):
    if amplitudes is None:
        amplitudes = [1.0] * len(frequencies)
    # Generate time axis
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    # Generate sine waves and sum them
    signal = sum([a * np.sin(2 * np.pi * f * t) for f, a in zip(frequencies, amplitudes)])
    if add_noise == True:
        noise_amplitude = 0.8  # Amplitude of the noise
        noise = noise_amplitude * np.random.normal(size=signal.shape)
        signal += noise
    # Normalize to 16-bit range
    signal_normalized = np.int16(signal / np.max(np.abs(signal)) * 32767)
    # Generate file name
    filename = '_'.join([f'{f}Hz' for f in frequencies]) + '_sine.wav'
    if add_noise == True:
        filename = 'noise_' + filename
    # Write to a WAV file
    wavfile.write('data/Sounds/Dirbtiniai/' + filename, sample_rate, signal_normalized)

# Sample rate, duration and frequencies
sample_rate = 44100  # Sample rate in Hz
duration_sec = 1.0  # Duration in seconds
amplitudes = None
frequencies = [50, 200]

generate_and_write(sample_rate, duration_sec, frequencies, amplitudes, add_noise=True)