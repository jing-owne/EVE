import warnings; warnings.filterwarnings('ignore')
import os; os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'; os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
import akshare as ak
try:
    df=ak.stock_zh_index_spot_em(symbol='000300')
    print('HS300 cols:')
    for c in df.columns: print(' ', c)
    print('data:')
    print(df)
except Exception as e:
    print('error:',e)
