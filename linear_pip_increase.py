import csv
import matplotlib.pyplot as plt

def check_linear_increase(bid_array):
    for i in range(len(bid_array) - 1):
        if bid_array[i] > bid_array[i + 1]:
            return False
    return True

def process_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        row_number = 1
        for row in reader:
            make_trade = int(row['make_trade'])
            bid_array = [float(x.strip('"')) for x in row['Bid Array'].strip('"""').split(',')]
            if make_trade == 1:
                if check_linear_increase(bid_array):
                    print(f"Row {row_number}: Bid array increased linearly.")
                    plt.plot(bid_array, label=f'Row {row_number} Bid Array')
                    plt.xlabel('Index')
                    plt.ylabel('Bid Value')
                    plt.title(f'Bid Array Visualization for Row {row_number}')
                    plt.legend()
                    plt.show()
            row_number += 1

# Example usage
process_csv(r'D:\FROM-MAIN-DISK\QUANTDATA\your_updated_file.csv')
