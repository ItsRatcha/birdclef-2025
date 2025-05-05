import os

def count_audio_files_by_prefix(folder_path):
    prefixes = ("XC", "iNat", "CSA")
    counts = {prefix: 0 for prefix in prefixes}
    csa_folder_counts = {}

    for root, _, files in os.walk(folder_path):
        csa_count_in_folder = 0
        for file in files:
            if file.endswith(".ogg"):
                for prefix in prefixes:
                    if file.startswith(prefix):
                        counts[prefix] += 1
                        if prefix == "CSA":
                            csa_count_in_folder += 1
                        break
        if csa_count_in_folder > 0:
            csa_folder_counts[root] = csa_count_in_folder

    return counts, csa_folder_counts

if __name__ == "__main__":
    folder_path = os.path.join(os.getcwd(), "train_audio")
    if os.path.exists(folder_path):
        result, csa_folders = count_audio_files_by_prefix(folder_path)
        for prefix, count in result.items():
            print(f"Number of .ogg files starting with {prefix}: {count}")
        
        print("\nFolders containing CSA files:")
        for folder, count in csa_folders.items():
            print(f"{folder}: {count} CSA files")
    else:
        print("The folder 'train_audio' does not exist.")