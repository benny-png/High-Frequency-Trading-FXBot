import csv

# Initialize variables to count the number of rows processed and store the lengths of arrays
row_count = 0

# Open and read the CSV file
with open('your_updated_file.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Read the header row and write it to the new CSV file
    header = next(csv_reader)

    # Open a new CSV file to write the valid rows
    with open('new_updated_file.csv', 'w', newline='') as new_csv_file:
        csv_writer = csv.writer(new_csv_file)

        # Write the header to the new CSV file
        csv_writer.writerow(header)

        # Iterate through the rows in the original CSV file
        for row in csv_reader:
            # Extract Bid Array, Ask Array, and Time Array from the row
            bid_array = row[5].strip('"""').split(',')
            ask_array = row[6].strip('"""').split(',')
            time_array = row[7].strip('"""').split(',')

            # Get the lengths of arrays
            bid_array_length = len(bid_array)
            ask_array_length = len(ask_array)
            time_array_length = len(time_array)

            # Check if lengths are the same for all arrays
            if bid_array_length != ask_array_length or bid_array_length != time_array_length:
                print(f"Arrays have different lengths in row {row_count + 2}. Skipping this row.")
                print(f"Bid Array Length: {bid_array_length}, Ask Array Length: {ask_array_length}, Time Array Length: {time_array_length}")
                # Skip this row by not writing it to the new CSV file
            else:
                # Write the valid row to the new CSV file
                csv_writer.writerow(row)

            # Increment row count
            row_count += 1

            # Print the lengths for preview
            if row_count <= 10:  # Print lengths for the first 10 rows
                print(f"Row {row_count}: Bid Array Length: {bid_array_length}, Ask Array Length: {ask_array_length}, Time Array Length: {time_array_length}")

# Print the total number of rows processed
print(f"Total rows processed: {row_count}")
