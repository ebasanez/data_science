# Calculate the rolling of 21 days volatility of any Darwin
import pandas as pd
df = pd.load_csv('LSV___XXX___.csv',index_col=0)
df.index = pd.to_datetime(df.index, unit='ms')
pd.resample('D').last().rolling(21).quote.std().dropna()
