import pandas as pd
from icecream import ic

# Load CSV data into pandas
data_path = 'Nifty 50 2000-2024 Weekly.csv'
data = pd.read_csv(data_path, parse_dates=['Date'], index_col='Date')

# Preprocess data to ensure numeric columns are correctly formatted
for column in ["close", "Open", "High", "Low"]:
    # Remove commas, handle non-numeric values by coercing errors, and fill any NaNs
    data[column] = pd.to_numeric(data[column].astype(str).str.replace(',', ''), errors='coerce')


# Drop any remaining rows with NaN after filling forward
data.dropna(inplace=True)
data = data.sort_index()

max_trades_interval = 8 # Invest at Every given interval 
investment_amount = 10000 / max_trades_interval

trades = []
Month_Trades = []
interval_idx = 1

def CanBuy(Dip, interval_trades, interval_idx, max_trades_interval = 4):
    

    # Return (False, 0) if max trades reached
    if len(interval_trades) >= max_trades_interval:
        return False, 0
    
    # If no trades in interval, ensure buy_amount is 4 at month-end (assuming interval_idx can be max_trades_interval or higher)
    if len(interval_trades) == 0 and interval_idx >= max_trades_interval:
        return True, max_trades_interval
    
    # Buy only if dip condition is met
    if not Dip and interval_idx <= 3:
        return False, 0

    # Calculate buy_amount based on interval without a trade
    interval_without_trade = max(0, interval_idx - len(interval_trades) - 1)
    buy_amount = 1 + interval_without_trade

    return True, buy_amount



for index, row in data.iterrows():
    print(f'interval {interval_idx}/{max_trades_interval}')    
    chnage = float(row['Change %'].replace('%',''))
    Dip = False
    
    if chnage < -0.49:
        Dip = True
        print(f'Dip:{Dip} | Change: {chnage}%')

    can_buy, buy_amount  = CanBuy(Dip, Month_Trades, interval_idx,max_trades_interval = max_trades_interval)
    

    if can_buy:
        print(f"interval {interval_idx} | {str(index.date())} : Buying {len(Month_Trades)+1} time in the month")
        volume = investment_amount / row['close']
        trade = {'date':index, "price":row['close'],  'volume': volume}
        print(f'need to buy: {buy_amount} times of SIP')
        for i in range(0,buy_amount):
            print(f'trade {i+1}/{buy_amount}')
            trades.append(trade)
            Month_Trades.append(trade)   
            print(f'Volume bought: {volume:.2f} at Price {row["close"]}')

    else:
        print(f"Can't buy: Dip: {Dip}, trades: {len(Month_Trades)}")

    if interval_idx == max_trades_interval:        
        print('reseting interval.')
        interval_idx = 1
        Month_Trades = []  
    else:
        interval_idx += 1
      
    
    print("-----")


def indian_currency_format(amount, precision=0):
    # Split the integer and decimal parts based on the precision
    amount_str = f"{amount:.{precision}f}"
    if precision > 0:
        integer_part, decimal_part = amount_str.split('.')
    else:
        integer_part, decimal_part = amount_str, ''
    
    # Perform Indian-style grouping on the integer part
    integer_part = integer_part[::-1]  # Reverse the string for easier grouping
    grouped = []
    # First group of three digits
    grouped.append(integer_part[:3])
    # Groups of two digits thereafter
    for i in range(3, len(integer_part), 2):
        grouped.append(integer_part[i:i+2])
    formatted_integer = ','.join(grouped)[::-1]  # Join and reverse back to normal

    # Combine the formatted integer part with the decimal part if it exists
    return f"₹{formatted_integer}" + (f".{decimal_part}" if decimal_part else "")




import pandas as pd
import matplotlib.pyplot as plt
history = pd.DataFrame(trades)

latest_price = history.iloc[-1]['price']
total_volume = history['volume'].sum()

plt.figure(figsize=(10, 5))
plt.plot(history['date'], history['volume'], marker='o')
# Formatting
plt.xlabel('Date')
plt.ylabel('Volume')
plt.title('Volume Bought Over Time')
plt.xticks(rotation=45)  # Rotate date labels for readability
plt.grid(True)

# Show plot
plt.tight_layout()  # Adjust layout to prevent clipping
plt.show(block=True)

currnt_price = total_volume * latest_price

print(f'Total Trades: {len(history)}' )
print(f'Total Investments: {indian_currency_format(len(history)*investment_amount)}' )
print(f'Total Volume: {total_volume:.2f}' )
print(f'Current Price: {indian_currency_format(currnt_price)}' )

pass