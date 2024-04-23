import pandas as pd
from tqdm import tqdm
import concurrent.futures

# Load your main training data
main_training_data = pd.read_csv('transformed_data.csv', parse_dates=['Start Timestamp', 'End Timestamp'])

# Load your bid and ask data
bid_ask_data = pd.read_csv('RAWTIMEURUSD2.csv', parse_dates=['DateTime'])

print('LOADED DATA')

# Set the time interval for grouping (5 minutes)
interval = pd.Timedelta(minutes=5)

# Round the 'DateTime' column to the nearest 5-minute interval
bid_ask_data['DateTime'] = bid_ask_data['DateTime'].dt.round(interval)

# Group the bid and ask data by 5-minute intervals
grouped_data = bid_ask_data.groupby('DateTime')


print(len(grouped_data))
# Initialize lists to store bid and ask arrays
bid_arrays = []
ask_arrays = []
time_arrays = [] 

# Define a function to process each interval
def process_interval(interval_start, group):
    bid_values = group['Bid'].tolist()
    ask_values = group['Ask'].tolist()
    time_values = group['Time'].tolist()  # Format time as "00:00:00.000"
    bid_array_str = '"' + ','.join(map(str, bid_values)) + '"'
    ask_array_str = '"' + ','.join(map(str, ask_values)) + '"'
    time_array_str = '"' + ','.join(map(str, time_values)) + '"'
    bid_arrays.append(bid_array_str)
    ask_arrays.append(ask_array_str)
    time_arrays.append(time_array_str)

print('starting Progress')
# Use tqdm to create a progress bar
with tqdm(total=len(grouped_data)) as pbar:
    # Process the intervals in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:  # You can also use ProcessPoolExecutor for true parallelism
        futures = [executor.submit(process_interval, interval_start, group) for interval_start, group in grouped_data]
        for future in concurrent.futures.as_completed(futures):
            pbar.update(1)


while len(bid_arrays) > len(main_training_data):
    bid_arrays.pop()  # Remove the last element from bid_arrays
    ask_arrays.pop()
    time_arrays.pop()# Remove the last element from ask_arrays
    
# Add the bid and ask arrays as new columns in the main training data
main_training_data['Bid Array'] = bid_arrays
main_training_data['Ask Array'] = ask_arrays
main_training_data['Time Array'] = time_arrays
# Save the updated main training data to a new CSV file
main_training_data.to_csv('updated_main_training_data.csv', index=False)
