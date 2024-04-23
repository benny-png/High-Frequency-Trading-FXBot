import csv

# Initialize variables to count the number of rows processed and store the lengths of arrays
row_count = 0

# Open and read the CSV file
with open('updated_main_training_data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Skip the header row
    next(csv_reader)
    
    # Iterate through the first 1000 rows
    for row in csv_reader:
        # Extract Bid Array and Ask Array from the row
        bid_array = row[5].strip('"""').split(',')
        ask_array = row[6].strip('"""').split(',')
        
        # Get the lengths of Bid and Ask arrays
        bid_array_length = len(bid_array)
        ask_array_length = len(ask_array)
        
        # Check if lengths are the same for Bid and Ask arrays
        if bid_array_length != ask_array_length:
            print(f"Arrays have different lengths in row {row_count + 2}.")
            print(f"Bid Array Length: {bid_array_length}, Ask Array Length: {ask_array_length}")
            # Stop processing if lengths are different
        
        # Increment row count
        row_count += 1
        
        # Print the lengths for preview
        if row_count <= 10:  # Print lengths for the first 10 rows
            print(f"Row {row_count}: Bid Array Length: {bid_array_length}, Ask Array Length: {ask_array_length}")

# Print the total number of rows processed
print(f"Total rows processed: {row_count}")
