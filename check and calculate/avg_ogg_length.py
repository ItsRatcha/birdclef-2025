import os
import statistics
import soundfile as sf
import matplotlib.pyplot as plt
import seaborn as sns

def get_ogg_file_lengths(folder_path):
    lengths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.ogg'):
                file_path = os.path.join(root, file)
                with sf.SoundFile(file_path) as audio_file:
                    lengths.append(len(audio_file) / audio_file.samplerate)
    return lengths

def remove_outliers(lengths):
    q1, q3 = statistics.quantiles(lengths, n=4)[0], statistics.quantiles(lengths, n=4)[2]
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return [length for length in lengths if lower_bound <= length <= upper_bound]

def calculate_statistics(lengths):
    stats = {
        "mean": statistics.mean(lengths),
        "median": statistics.median(lengths),
        "variance": statistics.variance(lengths),
        "std_dev": statistics.stdev(lengths),
        "min": min(lengths),
        "max": max(lengths),
        "25_percentile": statistics.quantiles(lengths, n=4)[0],
        "75_percentile": statistics.quantiles(lengths, n=4)[2],
    }
    stats["iqr"] = stats["75_percentile"] - stats["25_percentile"]
    return stats

def plot_and_save_graph(lengths, stats, output_file):
    plt.figure(figsize=(10, 6))
    # Increase the number of bins to better represent high variance
    plt.hist(lengths, bins=100, color='skyblue', alpha=0.7, edgecolor='black', label='Histogram')
    plt.axvline(stats["mean"], color='red', linestyle='dashed', linewidth=1, label=f'Mean: {stats["mean"]:.2f}s')
    plt.axvline(stats["median"], color='green', linestyle='dashed', linewidth=1, label=f'Median: {stats["median"]:.2f}s')
    plt.title('Histogram of OGG File Lengths')
    plt.xlabel('Length (seconds)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.savefig(output_file, format='svg')
    plt.show()

def main():
    folder_path = 'train_audio'  # Replace with the actual path to the train_audio folder
    output_file_with_outliers = 'ogg_file_lengths_with_outliers.svg'
    output_file_without_outliers = 'ogg_file_lengths_without_outliers.svg'

    lengths = get_ogg_file_lengths(folder_path)
    if not lengths:
        print("No OGG files found in the specified folder.")
        return

    print(f"Original number of files: {len(lengths)}")

    # Plot and save graph with outliers
    stats_with_outliers = calculate_statistics(lengths)
    print("Statistics with outliers (in seconds):")
    for key, value in stats_with_outliers.items():
        print(f"{key.capitalize()}: {value:.2f}")
    plot_and_save_graph(lengths, stats_with_outliers, output_file_with_outliers)
    print(f"Graph with outliers saved as {output_file_with_outliers}")

    # Remove outliers and process
    lengths_without_outliers = remove_outliers(lengths)
    print(f"Number of files after removing outliers: {len(lengths_without_outliers)}")

    stats_without_outliers = calculate_statistics(lengths_without_outliers)
    print("Statistics without outliers (in seconds):")
    for key, value in stats_without_outliers.items():
        print(f"{key.capitalize()}: {value:.2f}")
    plot_and_save_graph(lengths_without_outliers, stats_without_outliers, output_file_without_outliers)
    print(f"Graph without outliers saved as {output_file_without_outliers}")

if __name__ == "__main__":
    main()