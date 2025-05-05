import librosa
import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURABLE VARIABLES ===
audio_path = 'train_audio/baymac/iNat588759.ogg'  # Replace with your file
frame_length = 100  # Sliding window size in frames
use_mfcc = False  # Set to True to use MFCC instead of Mel spectrogram

# === LOAD AUDIO ===
y, sr = librosa.load(audio_path, sr=None)

# === EXTRACT FEATURES ===
if use_mfcc:
    features = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    feature_type = "MFCC"
else:
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    features = librosa.power_to_db(mel, ref=np.max)
    feature_type = "Log-Mel"

# === CALCULATE VARIANCE FOR EACH SLIDING WINDOW FRAME ===
def sliding_variance(spec, frame_len):
    half = frame_len // 2
    variances = []
    for t in range(spec.shape[1]):
        start = max(0, t - half)
        end = min(spec.shape[1], t + half + 1)
        window = spec[:, start:end]
        var = np.var(window)
        variances.append(var)
    return np.array(variances)

frame_variances = sliding_variance(features, frame_length)

# === PLOT VARIANCE OVER TIME ===
times = librosa.frames_to_time(np.arange(len(frame_variances)), sr=sr)

plt.figure(figsize=(10, 4))
plt.plot(times, frame_variances, label=f'{feature_type} Window Variance')
plt.xlabel("Time (s)")
plt.ylabel("Variance")
plt.title(f'Sliding Window Variance over Time ({feature_type})')
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.show()
