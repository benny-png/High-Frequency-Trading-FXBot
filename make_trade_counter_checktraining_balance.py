import pandas as pd

# Read the CSV file
print("STARTED....")
df = pd.read_csv(r'D:\FROM-MAIN-DISK\QUANTDATA\your_updated_file.csv')

# Assuming 'make_trade' is the column name where you want to count 0's and 1's
make_trade_counts = df['make_trade'].value_counts()

# Display the counts
print("Number of 0's:", make_trade_counts.get(0, 0))  # Get the count of 0's, default to 0 if not found
print("Number of 1's:", make_trade_counts.get(1, 0))  # Get the count of 1's, default to 0 if not found
