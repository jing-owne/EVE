import sys
print('Python:', sys.version)

try:
    import numpy
    print('numpy ok')
except Exception as e:
    print('numpy missing:', e)

try:
    import pandas
    print('pandas ok')
except Exception as e:
    print('pandas missing:', e)

try:
    import akshare as ak
    print('akshare ok:', ak.__version__)
except Exception as e:
    print('akshare missing:', e)
