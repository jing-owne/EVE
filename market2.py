import warnings; warnings.filterwarnings('ignore')
import os; os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'; os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
import akshare as ak
from datetime import datetime

print('=== Testing index hist APIs ===')

# try stock_zh_index_daily_em
for sym, label in [('sh000001', 'SH'), ('sz399001', 'SZ'), ('sz399006', 'CYB'), ('sh000300', 'HS300'), ('sh000016', 'SSE50')]:
    try:
        df = ak.stock_zh_index_daily_em(symbol=sym)
        if df is not None and not df.empty:
            last = df.iloc[-1]
            print(f'{label}({sym}): close={last.get("close",last.get("收盘价","?"))} rows={len(df)}')
        else:
            print(f'{label}: empty')
    except Exception as e:
        print(f'{label} fail: {str(e)[:80]}')

print()
print('=== Testing index_zh_a_hist ===')
for sym, label in [('000001', 'SH'), ('399001', 'SZ'), ('399006', 'CYB'), ('000300', 'HS300')]:
    try:
        df = ak.index_zh_a_hist(symbol=sym, period='daily', start_date='20260320', end_date='20260324')
        if df is not None and not df.empty:
            print(f'{label}: OK rows={len(df)}')
        else:
            print(f'{label}: empty')
    except Exception as e:
        print(f'{label} fail: {str(e)[:80]}')
