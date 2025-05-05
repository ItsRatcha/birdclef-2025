import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pyloudnorm as pyln
import soundfile as sf
import os

# === Settings ===
file_path = "train_audio/baymac/iNat588759.ogg"  # Replace with your file path
USE_MFCC = False   # Set to True for MFCC, False for Mel Spectrogram

# === Load Audio ===
y, sr = sf.read(file_path)
if y.ndim > 1:
    y = np.mean(y, axis=1)  # stereo to mono

# === Loudness Normalization ===
meter = pyln.Meter(sr)
loudness = meter.integrated_loudness(y)
y_norm = pyln.normalize.loudness(y, loudness, -23.0)

print(f"Original Loudness: {loudness:.2f} LUFS")
print(f"Normalized Loudness: {meter.integrated_loudness(y_norm):.2f} LUFS")

# === Save Normalized Audio ===
output_folder = "LUFS"
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_file = os.path.join(output_folder, "normalized_audio.wav")
sf.write(output_file, y_norm, sr)  # Save the normalized audio

print(f"Normalized audio saved to: {output_file}")

# === Feature Plotting Function ===
def plot_feature(y, sr, title, use_mfcc=False):
    if use_mfcc:
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        librosa.display.specshow(mfcc, x_axis='time', sr=sr)
        plt.title(title + " (MFCC)")
        plt.colorbar()
    else:
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        S_dB = librosa.power_to_db(S, ref=np.max)
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', fmax=8000)
        plt.title(title + " (Mel Spectrogram)")
        plt.colorbar(format='%+2.0f dB')

# === Plot Both Original & Normalized ===
plt.figure(figsize=(12, 5))

# Plot original audio
plt.subplot(1, 2, 1)
plot_feature(y, sr, f"Original (LUFS: {loudness:.2f})", use_mfcc=USE_MFCC)

# Plot normalized audio
normalized_loudness = meter.integrated_loudness(y_norm)
plt.subplot(1, 2, 2)
plot_feature(y_norm, sr, f"Normalized (LUFS: {normalized_loudness:.2f})", use_mfcc=USE_MFCC)

plt.tight_layout()
plt.show()
