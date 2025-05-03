import os
import sqlite3

# Path to the train_audio directory
train_audio_path = "train_audio/"

# Create a database to store folder ogg counts
output_db = "ogg_count.db"

# Path to the taxonomy database
taxonomy_db_path = "taxonomy.db" # Make sure this path is correct

# Define the name for the new joined table
joined_table_name = "joined_ogg_taxonomy"

# Connect to the output database (ogg_count.db)
conn = sqlite3.connect(output_db)
cursor = conn.cursor()

# --- Existing code to create and populate ogg_counts table ---

# Create a table to store folder ogg counts
cursor.execute("""
CREATE TABLE IF NOT EXISTS ogg_counts (
    id TEXT PRIMARY KEY,
    ogg_count INTEGER
)
""")

# Count .ogg files in each folder and insert into the database
# Note: This part could be optimized if run frequently by checking
# if the folder already exists in the DB before counting.
# For this example, INSERT OR REPLACE is fine for simplicity.
print(f"Counting .ogg files in folders under {train_audio_path}...")
processed_count = 0
for folder_name in os.listdir(train_audio_path):
    folder_path = os.path.join(train_audio_path, folder_name)
    if os.path.isdir(folder_path):
        ogg_count = len([f for f in os.listdir(folder_path) if f.endswith('.ogg')])
        cursor.execute("""
        INSERT OR REPLACE INTO ogg_counts (id, ogg_count)
        VALUES (?, ?)
        """, (folder_name, ogg_count))
        processed_count += 1
        if processed_count % 100 == 0:
            print(f"  Processed {processed_count} folders...")

# Commit changes for the ogg_counts table
conn.commit()
print(f"Finished counting. {processed_count} folders processed.")
print(f"ogg_counts table updated in {output_db}")

# --- New code to join with taxonomy.db and create the new table ---

print(f"\nAttempting to join data with {taxonomy_db_path}...")

try:
    # Attach the taxonomy database
    cursor.execute(f"ATTACH DATABASE '{taxonomy_db_path}' AS taxonomy_db;")
    print(f"Successfully attached {taxonomy_db_path}")

    # Drop the existing joined table if it exists
    cursor.execute(f"DROP TABLE IF EXISTS {joined_table_name};")
    print(f"Dropped existing table {joined_table_name} (if it existed).")

    # Create the new table for the joined data
    cursor.execute(f"""
    CREATE TABLE {joined_table_name} (
        id TEXT PRIMARY KEY,     -- Corresponds to ogg_counts.id and taxonomy_db.train_data.primary_label
        ogg_count INTEGER,       -- From ogg_counts
        common_name TEXT         -- From taxonomy_db.train_data
    )
    """)
    print(f"Created new table {joined_table_name}.")

    # Perform the join and insert data into the new table
    # We use aliases 'oc' for ogg_counts and 'td' for taxonomy_db.train_data
    cursor.execute(f"""
    INSERT INTO {joined_table_name} (id, ogg_count, common_name)
    SELECT
        oc.id,
        oc.ogg_count,
        td.common_name
    FROM
        ogg_counts AS oc
    JOIN
        taxonomy_db.train_data AS td ON oc.id = td.primary_label;
    """)
    print(f"Joined data inserted into {joined_table_name}.")

    # Commit the changes for the new table
    conn.commit()
    print("Changes committed.")

except sqlite3.OperationalError as e:
    print(f"Database error during join: {e}")
    print("Please ensure 'taxonomy.db' exists and contains a table named 'train_data' with columns 'primary_label' and 'common_name'.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Detach the taxonomy database (important cleanup)
    try:
        cursor.execute("DETACH DATABASE taxonomy_db;")
        print("Detached taxonomy_db.")
    except sqlite3.OperationalError:
        # This can happen if ATTACH failed in the first place
        pass

    # Close the connection
    conn.close()
    print(f"Connection to {output_db} closed.")

print("\nScript finished.")