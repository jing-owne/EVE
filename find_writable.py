import os, sys
paths_to_try = [
    os.path.join(os.path.expanduser('~'), 'Downloads'),
    os.path.join(os.path.expanduser('~'), 'Desktop'),
    'D:\\',
    'E:\\',
    'F:\\',
]
for p in paths_to_try:
    try:
        test = os.path.join(p, 'test_%d.txt' % os.getpid())
        open(test, 'w').close()
        os.remove(test)
        print('WRITABLE: ' + p)
    except Exception as e:
        print('NOT_WRITABLE: ' + p + ' - ' + str(e)[:60])
