import numpy as np
import soundfile as sf
import lameenc
import os

# Directory to save the MP3 output files
output_folder = "generated_frequencies"
os.makedirs(output_folder, exist_ok=True)

# Frequencies in Hz
frequencies = [
    174, 285, 396, 417, 432, 444, 528, 639, 741, 852,
    963, 100, 111, 120, 144, 174, 200, 210, 222, 285,
    300, 333, 350, 396, 417, 432, 444, 480, 500, 528,
    540, 555, 582, 600, 639, 693, 700, 741, 777, 800,
    852, 888, 900, 936, 963, 1000, 1020, 1111, 1200, 1222,
    136.1, 150, 174, 194, 210, 285, 324, 417, 528, 600,
    639, 852, 963, 7.83, 3, 6, 8, 10, 12, 15,
    20, 25, 30, 40, 50, 60, 70, 80, 90, 100,
    150, 200, 250, 300, 350, 400, 450, 500, 550, 600
]


# Audio properties
duration = 300  # Duration in seconds (5 minutes)
sample_rate = 44100  # Sample rate

def generate_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
    return (audio_data * 32767).astype(np.int16)  # Convert to 16-bit PCM format

def convert_wav_to_mp3(wav_filename, mp3_filename, sample_rate):
    # Read WAV file data for encoding
    audio_data, _ = sf.read(wav_filename, dtype='int16')
    
    # Encode to MP3
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(192)
    encoder.set_in_sample_rate(sample_rate)
    encoder.set_channels(1)
    encoder.set_quality(2)  # Highest quality

    mp3_data = encoder.encode(audio_data) + encoder.flush()

    with open(mp3_filename, "wb") as f:
        f.write(mp3_data)

# Generate and convert each frequency directly to MP3
for freq in frequencies:
    # Generate sine wave audio data
    audio_data = generate_sine_wave(freq, duration, sample_rate)

    # Save as temporary WAV file
    wav_filename = os.path.join(output_folder, f"{freq}Hz.wav")
    sf.write(wav_filename, audio_data, sample_rate)

    # Define MP3 filename and convert WAV to MP3
    mp3_filename = os.path.join(output_folder, f"{freq}Hz.mp3")
    convert_wav_to_mp3(wav_filename, mp3_filename, sample_rate)

    print(f"Generated {mp3_filename}")

    # Remove the intermediate WAV file
    os.remove(wav_filename)
