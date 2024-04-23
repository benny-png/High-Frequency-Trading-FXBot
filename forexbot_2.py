import MetaTrader5 as mt5
import pandas as pd
import time

print("DONE")

mt5.initialize()

def market_order():
    tick = mt5.symbol_info_tick('XAUUSD')
    pos1 = tick.bid
    mt5.Buy('XAUUSD', 0.01, price=None, comment=None, ticket=None)
    print('ORDER SET')
    return pos1

def close_position():
    mt5.Close('XAUUSD', ticket=None)
    print("[INFO] Closing position")

def sell_order():
    mt5.Sell('XAUUSD', 0.01, price=None, comment=None, ticket=None)
    print("[INFO] Placing sell order...")

def count_consecutive(pos1, pos2, threshold=0):
    """
    Count the consecutive bids where pos2 is greater than or equal to pos1.

    Parameters:
        pos1 (float): Previous bid.
        pos2 (float): Current bid.
        threshold (int): The threshold for consecutive bids.

    Returns:
        int: The number of consecutive bids.
    """
    if pos2 >= pos1:
        return threshold + 1
    else:
        return 0

def main():
    while True:
        sell_threshold = -3  # Initial sell threshold
        pos1 = market_order()  # Fetch the current tick outside the loop
        pips_count = 0  # Initialize pips count for linear increase
        while True:
            tick = mt5.symbol_info_tick('XAUUSD')
            pos2 = tick.bid

            pip_value = (pos2 - pos1)
            print(f'pip is {pip_value}')

            pips_count = count_consecutive(pos1, pos2, pips_count)

            if pips_count >= 5:  # If linear increase up to 5 pips
                print("[INFO] Linear increase detected, placing sell order...")
                mt5.Buy('XAUUSD', 0.01, price=None, comment=None, ticket=None)
                
                break

            if pip_value < 0:
                close_position()
                print("[INFO] Waiting for pip value to rise...")
                while pip_value <= 0:
                    tick = mt5.symbol_info_tick('XAUUSD')
                    pos2 = tick.bid
                    pip_value = (pos2 - pos1)
                    print(f'pip value is {pip_value}')
                    if pip_value <= sell_threshold:
                        sell_order()
                        sell_threshold -= 3  # Decrease the sell threshold by 3 pips for the next order
                        break
                print("[INFO] Pip value rose, setting next order automatically...")
                break

if __name__ == "__main__":
    main()
