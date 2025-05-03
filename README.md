This code is mostly for data analysis and preprocessing.

# What each file does

## 📁 check and calculate
### calculate_avg.py
Calculate mean, median, variance, standard deviation, min, max, percentile, interquartile and generate the histogram for the amount of .ogg files per animal ID

### check_rating.py
Count how many audio files get the rating of 0, 0.5, 1 , ..., 4, 4.5 and 5.

### ogg_length.py and ogg_length.txt
Count total hour for each animal ID. The code took time to execute so the output is in ogg_length.txt

### secondary_labels_count.py
Count total of .ogg files that has no secondary and how many that got the secondary.

## 📁 edit the csv
### split_call_type.py
split the Train.csv by call_type to the folder ```type of call/```.

### split_rating.py
Split the Train.csv by rating to the folder ```train.csv rating splitted/``` and count those rating counts.

### split_train.py
Create a new file ```train_cleaned.csv``` with only ```primary_label, secondary_labels, type, latitude, longitude``` to reduce the token count.

### low-resource.py
Create a new file ```ogg_count.db``` to browse species by ogg file count

---

## fourier.py
Pick and create a fourier of an ogg file to be created in fourier/ and can choose do delete frequency range.

## generate_charts.ipynb
Create (sort of) useful charts and graphs from train.csv

## generate_spectrograms.ipynb
Create spectrograms of any animal ID with the input of ID, max files and choice to create MFCC instead of Mel spectogram.

## map_visualizer.ipynb
Create a html file of the world map with latitude and longitude of every animal ID mapped.

## tokenizer.py
Count the token of .csv file, the default is using gpt2 to count the token of the file train_cleaned.csv

## turn_db.py
Turn the csv into database for ease of access
