import pandas as pd
import threading


# Read the original CSV file
df = pd.read_csv('2023.9.30EURUSD-M5-No Session.csv')

# Create a new DataFrame to store the transformed data
new_df = pd.DataFrame(columns=['Start Timestamp', 'End Timestamp', 'Change Label', 'Pip Difference', 'Volume'])

# Define a function to calculate the change label
def calculate_change_label(start_bid, end_bid):
    # Calculate the pip difference
    pip_difference = abs(end_bid - start_bid) * 10000  # Assuming 1 pip = 0.0001

    # Determine the change label
    if pip_difference >= 5:
        return 1
    else:
        return 0

def calculate_pip_difference(start_bid, end_bid):
    # Calculate the pip difference
    pip_difference = round((end_bid - start_bid) * 10000)  # Assuming 1 pip = 0.0001

    # Determine the change label
    return pip_difference


# Initialize variables for the 5-minute interval




# Iterate through the original DataFrame and create the new DataFrame
for i in range(1, len(df)):
    interval_start = pd.to_datetime(df.iloc[i]['DateTime'])
    try:
        interval_end = pd.to_datetime(df.iloc[i+1]['DateTime'])
    except:
        interval_end = '2023-09-28 23:55:00'
    start_bid = float(df.iloc[i]['Open'])
    end_bid = float(df.iloc[i]['Close'])
    volume = float(df.iloc[i]['Volume'])
    
    # Check if the current timestamp is still within the same 5-minute interval

    # Calculate the change label for the completed 5-minute interval
    change_label = calculate_change_label(start_bid, end_bid)
    pip_difference = calculate_pip_difference(start_bid, end_bid)
        
    new_df = new_df.append({'Start Timestamp': interval_start,
                            'End Timestamp': interval_end,
                            'Pip Difference': pip_difference,
                            'Volume' : volume,
                            'Change Label': change_label}, ignore_index=True)
        


        
    print(f'Processing row {i}/{len(df)}')

# Save the new DataFrame to a new CSV file
new_df.to_csv('transformed_data.csv', index=False)
