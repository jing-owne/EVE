import warnings; warnings.filterwarnings('ignore')
import os
os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'

import akshare as ak
from datetime import datetime

print('=== 实时大盘 ===')
try:
    df = ak.stock_zh_index_spot_em(symbol='000300')
    print(f'沪深300: {df["最新价"].iloc[0]} ({df["涨跌幅"].iloc[0]}%)')
except Exception as e:
    print(f'沪深300失败: {e}')

try:
    df = ak.stock_zh_index_spot_em(symbol='399006')
    print(f'创业板指: {df["最新价"].iloc[0]} ({df["涨跌幅"].iloc[0]}%)')
except Exception as e:
    print(f'创业板失败: {e}')

try:
    df = ak.stock_zh_index_spot_em(symbol='000001')
    print(f'上证指数: {df["最新价"].iloc[0]} ({df["涨跌幅"].iloc[0]}%)')
except Exception as e:
    print(f'上证失败: {e}')

try:
    df = ak.stock_zh_index_spot_em(symbol='000016')
    print(f'上证50: {df["最新价"].iloc[0]} ({df["涨跌幅"].iloc[0]}%)')
except Exception as e:
    print(f'上证50失败: {e}')

print('')
print('=== 涨跌停统计 ===')
try:
    zt = ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d'))
    print(f'涨停: {len(zt)}家')
except Exception as e:
    print(f'涨停失败: {e}')

try:
    dt = ak.stock_zt_pool_strong_em(date=datetime.now().strftime('%Y%m%d'))
    print(f'跌停: {len(dt)}家')
except Exception as e:
    print(f'跌停失败: {e}')

print('')
print('=== 全市场成交 ===')
try:
    sh = ak.stock_zh_a_spot_em()
    amt = float(sh['成交额'].sum()) / 1e8
    print(f'全市场成交额: {amt:.0f}亿')
    print(f'全市场股票数: {len(sh)}')
except Exception as e:
    print(f'成交额失败: {e}')
