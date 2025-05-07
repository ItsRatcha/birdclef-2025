import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

# Variable to accept the local path of the .ogg file
ogg_file_path = "train_audio/48124/CSA03598.ogg"  # Replace with the actual file path

# List of different numbers of triangular Mel bandpass filters
n_mels_options = [20, 40, 60, 80, 100]  # Example values; adjust as needed

def generate_mel_spectrograms_with_varied_filters(ogg_file_path, n_mels_list):
    """
    Loads audio, calculates Mel spectrograms using different numbers of Mel filters
    for data augmentation according to the paper's method.

    Args:
        ogg_file_path (str): Path to the input audio file.
        n_mels_list (list): A list of integers, where each integer is
                            a different number of Mel filters to use.

    Returns:
        list: A list of tuples, each containing (mel_spectrogram, sr, n_mels_used).
              These are the augmented data representations (pictures).
    """
    try:
        # Load the .ogg file
        audio, sr = librosa.load(ogg_file_path, sr=None)
        print(f"Loaded audio file: {ogg_file_path} with sample rate {sr}")
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return []

    augmented_spectrograms = []

    # Generate a Mel spectrogram for each specified number of filters
    for n_mels in n_mels_list:
        print(f"Generating Mel spectrogram with {n_mels} Mel filters...")
        mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=n_mels)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        augmented_spectrograms.append((mel_spec_db, sr, n_mels))

    return augmented_spectrograms

def plot_generated_spectrograms(spectrogram_data):
    """
    Plots the generated Mel spectrograms.

    Args:
        spectrogram_data (list): List of tuples from generate_mel_spectrograms.
    """
    print("\nPlotting generated spectrograms:")
    for i, (mel_spec_db, sr, n_mels) in enumerate(spectrogram_data):
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title(f'Mel Spectrogram ({n_mels} Mel filters)')
        plt.tight_layout()
        plt.show()
        print(f"Displayed plot for {n_mels} Mel filters.")

# Example usage
if __name__ == "__main__":
    if os.path.exists(ogg_file_path):
        # Generate the augmented spectrograms using the specified filter numbers
        generated_spectrograms = generate_mel_spectrograms_with_varied_filters(ogg_file_path, n_mels_options)

        if generated_spectrograms:
            print(f"\nGenerated {len(generated_spectrograms)} augmented spectrograms.")
            # Plot the results to see the variations
            plot_generated_spectrograms(generated_spectrograms)

            # These 'generated_spectrograms' (the mel_spec_db arrays) are the
            # "pictures" you would feed into your CNN model, according to the paper's
            # data augmentation strategy. Each element in the list is an augmented version.
    else:
        print(f"Error: The file '{ogg_file_path}' does not exist.")