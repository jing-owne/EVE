import warnings; warnings.filterwarnings('ignore')
import os; os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'; os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
import akshare as ak
from datetime import datetime

# try index_zh_a_hist
try:
    df = ak.index_zh_a_hist(symbol='000300', period='daily', start_date='20260320', end_date='20260324')
    print('hist OK'); print(df.to_string())
except Exception as e:
    print('hist fail:', e)
