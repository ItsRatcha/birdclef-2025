import os
import soundfile as sf

def get_audio_duration(file_path):
    with sf.SoundFile(file_path) as f:
        return len(f) / f.samplerate  # duration in seconds

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"

def count_audio_durations(base_path="train_audio"):
    id_durations = []

    with os.scandir(base_path) as entries:
        for entry in entries:
            if entry.is_dir():
                total_seconds = 0
                with os.scandir(entry.path) as files:
                    for file in files:
                        if file.name.endswith(".ogg"):
                            file_path = file.path
                            try:
                                total_seconds += get_audio_duration(file_path)
                            except RuntimeError:
                                print(f"Couldn't read {file_path}, skipping.")

                id_durations.append((entry.name, total_seconds))

    # Sort by total duration (ascending)
    id_durations.sort(key=lambda x: x[1])

    # Convert durations to formatted strings
    return [(id, format_duration(seconds)) for id, seconds in id_durations]

# Example usage
durations = count_audio_durations()
for id, formatted_duration in durations:
    print(f"{id}: {formatted_duration}")
