import os

import matplotlib.pyplot as plt

def display_spectrograms(main_folder, sub_folder, max_png_to_show):
    """
    Display multiple spectrogram PNGs from a specified folder.

    Parameters:
        main_folder (str): Path to the main folder containing subfolders of spectrograms.
        sub_folder (str): Name of the subfolder to pick inside the main folder.
        max_png_to_show (int): Maximum number of PNG files to display.
    """
    folder_path = os.path.join(main_folder, sub_folder)
    
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    # Get all PNG files in the folder
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    
    if not png_files:
        print(f"No PNG files found in '{folder_path}'.")
        return

    # Limit the number of PNGs to display
    png_files = png_files[:max_png_to_show]

    # Display the spectrograms
    plt.figure(figsize=(15, 5))
    for i, png_file in enumerate(png_files):
        img_path = os.path.join(folder_path, png_file)
        img = plt.imread(img_path)
        plt.subplot(1, len(png_files), i + 1)
        plt.imshow(img)
        plt.axis('off')
        plt.title(png_file)
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Example usage
    main_folder = "spectrograms"  # Path to the main folder
    sub_folder = "42087"  # Subfolder to pick
    max_png_to_show = 5  # Maximum number of PNGs to display

    display_spectrograms(main_folder, sub_folder, max_png_to_show)