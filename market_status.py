import warnings; warnings.filterwarnings('ignore')
import os; os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'; os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
import akshare as ak
from datetime import datetime

results = {}

# === 涨跌停（这个接口稳定）===
try:
    zt = ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d'))
    results['zt'] = len(zt)
except:
    results['zt'] = 0

try:
    dt = ak.stock_zt_pool_strong_em(date=datetime.now().strftime('%Y%m%d'))
    results['dt'] = len(dt)
except:
    results['dt'] = 0

# === 大盘指数（多源备选）===
# 方案1: stock_zh_index_spot_em (参数用不同格式)
apis_to_try = [
    ('em_single', lambda: ak.stock_zh_index_spot_em(symbol='000300')),
    ('em_list', lambda: ak.stock_zh_index_spot_em()),
]

idx_data = {}
for name, fn in apis_to_try:
    try:
        df = fn()
        if df is not None and not df.empty:
            cols = df.columns.tolist()
            val_col = [c for c in cols if '最新' in c or '当前' in c or 'price' in c.lower()][0]
            chg_col = [c for c in cols if '涨跌幅' in c or '涨跌' in c][0]
            nm_col = [c for c in cols if '名称' in c or 'name' in c.lower()][0]
            
            if name == 'em_list':
                for _, row in df.iterrows():
                    nm = str(row[nm_col])
                    if '沪深300' in nm or '000300' in str(row.get(nm_col,'')):
                        idx_data['hs300'] = (float(row[val_col]), float(row[chg_col]))
                    if '创业板' in nm:
                        idx_data['cyb'] = (float(row[val_col]), float(row[chg_col]))
                    if '上证指数' in nm or '上证' in nm:
                        idx_data['sh'] = (float(row[val_col]), float(row[chg_col]))
                    if '上证50' in nm:
                        idx_data['sse50'] = (float(row[val_col]), float(row[chg_col]))
            break
    except Exception as e:
        continue

results['idx'] = idx_data
results['ts'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 输出
print('DONE')
print('zt:', results['zt'])
print('dt:', results['dt'])
print('idx:', results['idx'])
