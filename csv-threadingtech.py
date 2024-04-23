import pandas as pd
import threading

# Read the original CSV file
df = pd.read_csv('RAWTICKURUSD.csv')

# Function to calculate the change label
def calculate_change_label(start_bid, end_bid):
    # Calculate the pip difference
    pip_difference = abs(end_bid - start_bid) * 10000  # Assuming 1 pip = 0.0001

    # Determine the change label
    if pip_difference >= 5:
        return 1
    else:
        return 0

# Function to process a section of the DataFrame
def process_section(start_idx, end_idx, section_df):
    for i in range(start_idx, end_idx):
        current_timestamp = pd.to_datetime(section_df.iloc[i]['DateTime'])
        current_bid = float(section_df.iloc[i]['Bid'])

        if (current_timestamp - interval_start).total_seconds() < 300:
            interval_end = current_timestamp
        else:
            change_label = calculate_change_label(start_bid, current_bid)
            new_df.loc[len(new_df)] = [interval_start, interval_end, change_label]
            interval_start = current_timestamp
            interval_end = current_timestamp
            start_bid = current_bid

        print(f'Processed row {i}/{end_idx}')

# Initialize variables for the 5-minute interval
interval_start = pd.to_datetime(df.iloc[0]['DateTime'])
interval_end = interval_start
start_bid = float(df.iloc[0]['Bid'])

# Create a new DataFrame to store the transformed data
new_df = pd.DataFrame(columns=['Start Timestamp', 'End Timestamp', 'Change Label'])

# Define the number of threads (adjust as needed)
num_threads = 4

# Calculate the chunk size for each thread
chunk_size = len(df) // num_threads

# Create a list to store thread objects
threads = []

# Split the DataFrame into sections and process them concurrently
for i in range(num_threads):
    start_idx = i * chunk_size
    end_idx = start_idx + chunk_size if i < num_threads - 1 else len(df)
    section_df = df[start_idx:end_idx]

    thread = threading.Thread(target=process_section, args=(start_idx, end_idx, section_df))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Save the new DataFrame to a new CSV file
new_df.to_csv('transformed_data.csv', index=False)
