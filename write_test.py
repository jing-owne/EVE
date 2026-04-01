import os, sys
try:
    path = os.path.join(os.environ['TEMP'], 'test_py.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('test write ok')
    print('write ok to:', path)
except Exception as e:
    print('write fail:', e)
    # try writable dir
    for test_dir in ['C:\\Users\\admin\\AppData\\Local\\Temp', 'C:\\temp', 'C:\\Users\\admin\\Desktop']:
        try:
            tp = os.path.join(test_dir, 'test.txt')
            with open(tp, 'w') as tf:
                tf.write('ok')
            print('writable:', test_dir)
            break
        except:
            pass
