import warnings; warnings.filterwarnings('ignore')
import os; os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'; os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
import akshare as ak
try:
    df=ak.stock_zh_index_spot_em()
    print('All indices:')
    print(df.head(20))
    print('columns:',list(df.columns))
    print('total rows:',len(df))
    # find hs300
    mask = df.apply(lambda row: '300' in str(row.values) or '沪深' in str(row.values), axis=1)
    print('HS300 related:')
    print(df[mask])
except Exception as e:
    import traceback; traceback.print_exc()
    print('error:',e)
