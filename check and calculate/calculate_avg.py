import os
import numpy as np
import matplotlib.pyplot as plt # Optional: for histogram visualization
from collections import Counter
import sys # To exit gracefully if folder not found

# --- Configuration ---
BASE_FOLDER = 'train_audio'  # The main folder containing ID subfolders
FILE_EXTENSION = '.ogg'     # The file type to count (case-insensitive)
# -------------------

def analyze_audio_counts(base_folder, file_extension):
    """
    Analyzes the distribution of audio files within ID subfolders.

    Args:
        base_folder (str): Path to the main directory containing ID subfolders.
        file_extension (str): The file extension to count (e.g., '.ogg').

    Returns:
        dict: A dictionary containing calculated statistics, or None if an error occurs.
            Returns the raw counts per ID as well: {'stats': {...}, 'id_counts': {...}}
    """
    if not os.path.isdir(base_folder):
        print(f"Error: Base folder '{base_folder}' not found or is not a directory.")
        return None

    id_file_counts = {}
    file_extension_lower = file_extension.lower()
    processed_ids = 0
    total_files_found = 0

    print(f"Scanning '{base_folder}' for subfolders and '{file_extension}' files...")

    # Iterate through items in the base folder
    for item_name in os.listdir(base_folder):
        item_path = os.path.join(base_folder, item_name)

        # Check if it's a directory (an ID folder)
        if os.path.isdir(item_path):
            id_name = item_name
            count = 0
            try:
                # Iterate through files within the ID folder
                for filename in os.listdir(item_path):
                    file_path = os.path.join(item_path, filename)
                    # Check if it's a file and has the correct extension
                    if os.path.isfile(file_path) and filename.lower().endswith(file_extension_lower):
                        count += 1
            except OSError as e:
                 print(f"Warning: Could not read files in folder '{item_path}'. Skipping. Error: {e}")
                 continue # Skip this ID if we can't read its contents

            id_file_counts[id_name] = count
            processed_ids += 1
            total_files_found += count
            # Optional: print progress periodically
            # if processed_ids % 100 == 0:
            #    print(f"  Processed {processed_ids} IDs...")

    print(f"Scan complete. Found {processed_ids} potential ID folders.")

    if not id_file_counts:
        print("No valid ID folders containing files were found.")
        return {'stats': {}, 'id_counts': {}} # Return empty structure

    # Extract the counts into a list for statistical analysis
    counts_list = list(id_file_counts.values())
    counts_array = np.array(counts_list)

    # Calculate statistics
    stats = {}
    stats['num_ids'] = len(counts_array)
    stats['total_files'] = int(np.sum(counts_array)) # Use int() for cleaner display
    if stats['num_ids'] > 0:
        stats['mean'] = np.mean(counts_array)
        stats['median'] = np.median(counts_array)
        stats['variance'] = np.var(counts_array)
        stats['std_dev'] = np.std(counts_array)
        stats['min'] = int(np.min(counts_array))     # Use int() for cleaner display
        stats['max'] = int(np.max(counts_array))     # Use int() for cleaner display
        # Additional useful stats
        stats['25th_percentile'] = np.percentile(counts_array, 25)
        stats['75th_percentile'] = np.percentile(counts_array, 75)
        stats['iqr'] = stats['75th_percentile'] - stats['25th_percentile'] # Interquartile Range
    else:
        # Handle case with zero valid IDs found after initial scan
         print("No valid file counts obtained for statistics.")
         stats.update({ # Set defaults for stats if no data
            'mean': 0, 'median': 0, 'variance': 0, 'std_dev': 0,
            'min': 0, 'max': 0, '25th_percentile': 0, '75th_percentile': 0, 'iqr': 0
         })


    return {'stats': stats, 'id_counts': id_file_counts, 'counts_array': counts_array}


def print_analysis_results(results):
    """Prints the calculated statistics in a formatted way."""
    if not results or not results['stats']:
        print("No analysis results to display.")
        return

    stats = results['stats']
    print("\n" + "=" * 40)
    print("      Audio File Count Analysis")
    print("=" * 40)
    print(f"Base Folder Searched:   '{BASE_FOLDER}'")
    print(f"File Extension Counted: '{FILE_EXTENSION}'")
    print("-" * 40)
    print(f"Total IDs Analyzed:     {stats.get('num_ids', 'N/A')}")
    print(f"Total Files Found:      {stats.get('total_files', 'N/A')}")
    print("-" * 40)
    print("Statistics (per ID):")
    if stats.get('num_ids', 0) > 0:
        print(f"  Mean:                 {stats['mean']:.2f}")
        print(f"  Median:               {stats['median']:.2f}") # Median can be float if even number of IDs
        print(f"  Variance:             {stats['variance']:.2f}")
        print(f"  Standard Deviation:   {stats['std_dev']:.2f}")
        print(f"  Minimum Count:        {stats['min']}")
        print(f"  Maximum Count:        {stats['max']}")
        print(f"  25th Percentile:      {stats['25th_percentile']:.2f}")
        print(f"  75th Percentile:      {stats['75th_percentile']:.2f}")
        print(f"  Interquartile Range:  {stats['iqr']:.2f}")
    else:
         print("  (No data for statistics)")
    print("=" * 40)

    # Optional: Print some example counts
    # print("\nSample ID Counts:")
    # count = 0
    # for id_name, file_count in results.get('id_counts', {}).items():
    #     print(f"  {id_name}: {file_count}")
    #     count += 1
    #     if count >= 5: # Print first 5
    #         break


def plot_histogram(counts_array, stats):
    """Generates and displays a histogram of the file counts."""
    if counts_array is None or len(counts_array) == 0:
        print("\nCannot plot histogram: No count data available.")
        return

    if 'matplotlib' not in sys.modules:
         print("\nMatplotlib not installed. Skipping histogram.")
         print("Install it using: pip install matplotlib")
         return

    plt.figure(figsize=(12, 6))
    # Determine reasonable number of bins, avoid too many if max count is huge
    max_count = stats.get('max', 1)
    num_bins = min(max_count + 1, 50) # Cap bins at 50 or use max_count if smaller
    if max_count > 0: # Ensure bins are at least 1
        num_bins = max(1, num_bins)
    else:
        num_bins = 1 # Handle edge case where max count is 0

    plt.hist(counts_array, bins=num_bins, edgecolor='black', alpha=0.7)
    plt.title(f'Distribution of {FILE_EXTENSION} File Counts per ID')
    plt.xlabel(f'Number of {FILE_EXTENSION} Files')
    plt.ylabel('Number of IDs')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add vertical lines for mean and median
    mean_val = stats.get('mean')
    median_val = stats.get('median')
    if mean_val is not None:
        plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
    if median_val is not None:
        plt.axvline(median_val, color='green', linestyle='dashed', linewidth=1.5, label=f'Median: {median_val:.2f}')

    plt.legend()
    plt.tight_layout() # Adjust layout to prevent labels overlapping
    print("\nGenerating histogram...")
    plt.show()


# --- Main Execution ---
if __name__ == "__main__":
    analysis_results = analyze_audio_counts(BASE_FOLDER, FILE_EXTENSION)

    if analysis_results:
        print_analysis_results(analysis_results)
        # Optional: Plot histogram
        plot_histogram(analysis_results.get('counts_array'), analysis_results.get('stats'))
    else:
        # Error message already printed in analyze_audio_counts
        sys.exit(1) # Exit with an error code