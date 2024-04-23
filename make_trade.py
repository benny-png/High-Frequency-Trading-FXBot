import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('updated_main_training_data.csv')

# Initialize an empty list to store the "make_trade" values
make_trade_values = []

# Get the total number of rows in the DataFrame
total_rows = len(df)

# Iterate through the rows of the DataFrame
for index, row in df.iterrows():
    if index == total_rows - 1:
        make_trade_values.append(0)  # The last row cannot have a next row with "Change Label" equal to 1
    else:
        # Check if the next row has "Change Label" equal to 1
        if df.at[index + 1, 'Change Label'] == 1:
            make_trade_values.append(1)
        else:
            make_trade_values.append(0)

    # Print progress
    print(f"Processed row {index + 1} of {total_rows}")

# Add the "make_trade" column to the DataFrame
df['make_trade'] = make_trade_values

# Save the updated DataFrame to a new CSV file
df.to_csv('your_updated_file.csv', index=False)

# Print completion message
print("Processing complete.")
