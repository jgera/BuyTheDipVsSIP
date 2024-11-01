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

SIP_Interval = 1  # Invest Every 4th week approx end of month
idx = 1
SIP_Amount = 2500

trades = []

for index, row in data.iterrows():   
    
    if idx < SIP_Interval:
        print(f"Week {idx}: waiting.")
        idx+=1
        
        continue
    print(f"Week {idx} | {str(index.date())} : Buying.")    
    
    idx = 1
    VolumeBought = SIP_Amount / row['close']
    
    print(f'buy: {VolumeBought:.2f}')
    trades.append({'date':index, "price":row['close'],  'volume': VolumeBought})
    
    
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
print(f'Total Investments: {indian_currency_format(len(history)*SIP_Amount)}' )
print(f'Total Volume: {total_volume:.2f}' )
print(f'Current Price: {indian_currency_format(currnt_price)}' )

pass