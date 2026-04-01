import warnings; warnings.filterwarnings('ignore')
import os; os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'; os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
import akshare as ak
from datetime import datetime, timedelta

today = datetime.now().strftime('%Y%m%d')

# try hist api for index
print('=== hist api for indices ===')
for code, name in [('000001', 'sh000001'), ('399001', 'sh399001'), ('399006', 'cyb'), ('000300', 'hs300')]:
    try:
        df = ak.stock_zh_index_daily_em(symbol=code)
        if not df.empty:
            last = df.iloc[-1]
            print(f'{name}: close={last["close"]}, chg={((last["close"]-last["open"])/last["open"]*100):.2f}%')
    except Exception as e:
        print(f'{name} hist fail: {e}')
