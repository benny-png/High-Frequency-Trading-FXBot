from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from mt5linux import MetaTrader5
import pandas as pd
import time

mt5 = MetaTrader5()
mt5.initialize()

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get('https://www.dailyfx.com/eur-usd')

def market_order():
    pos1pd = mt5.copy_rates_from_pos('EURUSD', mt5.TIMEFRAME_M1, 1, 10)
    pos1dt = pd.DataFrame(pos1pd)
    global pos1
    global pos1q

    pos1q = pos1dt.iloc[-1].close
    x = str(pos1q)
    pos1 = float(x[3:6])
    mt5.Buy('EURUSD', 0.01, price=None, comment=None, ticket=None)
    print('ORDER SET')

def close_position():
    mt5.Close('EURUSD', ticket=None)
    print("[INFO] Closing position")

def sell_order():
    mt5.Sell('EURUSD', 0.01, price=None, comment=None, ticket=None)
    print("[INFO] Placing sell order...")

def main():
    sell_threshold = -3  # Initial sell threshold
    while True:
        market_order()

        while True:
            pos2q = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='dfx-singleInstrument__price dfx-rate dfx-font-size-3 font-weight-bold text-right dfx-singleInstrument__bid']"))).get_attribute("data-value")
            print(pos1q)
            print(pos2q)
            pos2 = float(pos2q[3:6])
            pip_value = pos2 - pos1
            print(f'pip is {pip_value}')

            if pos2 == pos1:
                print('[INFO] Still the same first bar ...')
                continue

            if pip_value >= 3:
                close_position()
                break

            if pip_value < 0:
                print("[INFO] Waiting for pip value to rise...")
                while pip_value <= 0:
                    pos2q = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='dfx-singleInstrument__price dfx-rate dfx-font-size-3 font-weight-bold text-right dfx-singleInstrument__bid']"))).get_attribute("data-value")
                    pos2 = float(pos2q[3:6])
                    pip_value = pos2 - pos1
                    print(f'pip value is {pip_value}')
                    if pip_value <= sell_threshold:
                        sell_order()
                        sell_threshold -= 3  # Decrease the sell threshold by 3 pips for the next order
                print("[INFO] Pip value rose, setting next order automatically...")
                break

if __name__ == "__main__":
    main()
