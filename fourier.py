import os
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

# === CHOOSE ROOT ===
root_folder = "train_audio"

# === SELECT SUBFOLDER ===
subfolders = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]
if not subfolders:
    print("No subfolders found in train_audio.")
    exit()

print("\nSelect a folder:")
for i, folder in enumerate(subfolders):
    print(f"{i}: {folder}")
folder_input = input("Enter folder number or code: ").strip()

# Determine selected folder based on input
if folder_input.isdigit():
    folder_index = int(folder_input)
    if folder_index < 0 or folder_index >= len(subfolders):
        print("Invalid folder number.")
        exit()
    selected_folder = os.path.join(root_folder, subfolders[folder_index])
elif folder_input in subfolders:
    selected_folder = os.path.join(root_folder, folder_input)
else:
    print("Invalid folder code.")
    exit()

# === SELECT FILE ===
files = [f for f in os.listdir(selected_folder) if f.endswith('.ogg')]
if not files:
    print("No .ogg files found in selected folder.")
    exit()

print("\nSelect a file:")
for i, fname in enumerate(files):
    print(f"{i}: {fname}")
file_index = int(input("Enter file number: "))
filename = os.path.join(selected_folder, files[file_index])

# === LOAD AUDIO ===
data, samplerate = sf.read(filename)
if data.ndim > 1:
    data = np.mean(data, axis=1)  # stereo to mono

# === CREATE OUTPUT FOLDER ===
fourier_folder = os.path.join("fourier", os.path.basename(selected_folder))
os.makedirs(fourier_folder, exist_ok=True)

# === FFT ===
fft_result = np.fft.fft(data)
frequencies = np.fft.fftfreq(len(data), d=1/samplerate)
magnitude = np.abs(fft_result)

# === SAVE FOURIER PLOT ===
plt.figure(figsize=(12, 6))
plt.plot(frequencies[:len(frequencies)//2], magnitude[:len(magnitude)//2])
plt.title(f"Fourier Transform of {files[file_index]}")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()

fourier_plot_path = os.path.join(fourier_folder, f"{os.path.splitext(files[file_index])[0]}_fourier.png")
plt.savefig(fourier_plot_path)
plt.close()
print(f"Fourier plot saved to: {fourier_plot_path}")

# === ASK TO EDIT AUDIO ===
edit_choice = input("\nDo you want to edit the audio file? (yes/no): ").strip().lower()
if edit_choice == "yes":
    # === DELETE FREQ RANGE ===
    low_freq = float(input("Enter LOW frequency to delete (Hz): "))
    high_freq = float(input("Enter HIGH frequency to delete (Hz): "))
    mask = (np.abs(frequencies) >= low_freq) & (np.abs(frequencies) <= high_freq)
    fft_result[mask] = 0
    filtered_signal = np.fft.ifft(fft_result).real
    output_filename = f"filtered_{files[file_index].replace('.ogg', '.wav')}"
    output_path = os.path.join(selected_folder, output_filename)
    sf.write(output_path, filtered_signal, samplerate)
    print(f"\nFiltered audio saved to: {output_path}")
else:
    print("No edits made to the audio file.")
