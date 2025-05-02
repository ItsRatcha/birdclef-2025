import csv
import os

def split_csv_by_rating(input_filename='train.csv', rating_column_index=5):
    """
    Splits a CSV file into multiple files based on the rating in intervals of 0.5
    and saves them into a new subdirectory.

    Args:
        input_filename (str): The name of the input CSV file (default 'train.csv').
        rating_column_index (int): The 0-based index of the rating column
                                (default 5 for the 6th column).
    """

    # Define the name of the output directory
    output_directory = "train.csv rating splitted"

    # Dictionary to hold rows grouped by rating intervals (0, 0.5, ..., 5)
    grouped_data = {i / 2: [] for i in range(11)}
    header = None
    rows_processed = 0

    print(f"Attempting to read '{input_filename}'...")

    # --- Read the input CSV file ---
    try:
        with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)

            try:
                header = next(reader)
                print(f"Header found: {header}")
            except StopIteration:
                print(f"Warning: '{input_filename}' appears to be empty or contains only a header.")

            line_num = 1  # Start counting after header
            for row in reader:
                line_num += 1
                rows_processed += 1

                if len(row) > rating_column_index:
                    rating_str = row[rating_column_index]

                    try:
                        rating = float(rating_str)

                        if 0 <= rating <= 5:
                            # Round the rating to the nearest 0.5
                            rounded_rating = round(rating * 2) / 2
                            grouped_data[rounded_rating].append(row)

                    except ValueError:
                        print(f"Warning: Row {line_num} has non-numeric rating '{rating_str}', skipping row: {row}")

                else:
                    print(f"Warning: Row {line_num} has insufficient columns ({len(row)}), expected at least {rating_column_index + 1}. Skipping row: {row}")

    except FileNotFoundError:
        print(f"Error: The input file '{input_filename}' was not found in the current directory.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading '{input_filename}': {e}")
        return

    # --- Create the output directory if it doesn't exist ---
    try:
        os.makedirs(output_directory, exist_ok=True)
        print(f"\nEnsured directory '{output_directory}' exists.")
    except OSError as e:
        print(f"Error: Could not create directory '{output_directory}': {e}")
        # If directory creation fails, we cannot proceed
        return

    # --- Write the output CSV files ---
    if header is None:
        print("Cannot write output files as no header was read from the input file.")
        return

    print(f"\nFinished reading {rows_processed} data rows. Writing output files to '{output_directory}'...")

    # Iterate through the rating intervals we want to split by (0, 0.5, ..., 5)
    for rating in grouped_data.keys():
        # Construct the base filename
        base_output_filename = f"data with {rating} rating.csv"
        # Construct the full path using os.path.join for cross-platform compatibility
        full_output_path = os.path.join(output_directory, base_output_filename)

        rows_to_write = grouped_data.get(rating, [])

        try:
            # Open output file for writing using the full path
            with open(full_output_path, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)

                writer.writerow(header)

                if rows_to_write:
                    writer.writerows(rows_to_write)
                    print(f"Created '{full_output_path}' with {len(rows_to_write)} data rows.")
                else:
                    print(f"Created '{full_output_path}' with header only (no data for rating {rating}).")

        except Exception as e:
            print(f"An error occurred while writing '{full_output_path}': {e}")

    print("\nSplitting process finished.")


# --- Main execution block ---
if __name__ == "__main__":
    split_csv_by_rating(input_filename='train.csv', rating_column_index=5)