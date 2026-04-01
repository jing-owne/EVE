import os, sys
workspace = 'C:/Users/admin/.qclaw/workspace'
test_file = os.path.join(workspace, 'test_%d.txt' % os.getpid())
print('Testing write to:', test_file)
try:
    with open(test_file, 'w') as f:
        f.write('test')
    print('SUCCESS - wrote test file')
    os.remove(test_file)
    print('SUCCESS - deleted test file')
except Exception as e:
    print('FAILED:', e)
    # Try to understand WHY
    import stat
    try:
        st = os.stat(workspace)
        print('Workspace stat:', oct(st.st_mode))
        print('Is dir:', stat.S_ISDIR(st.st_mode))
        print('Readable:', os.access(workspace, os.R_OK))
        print('Writable by Python process?', os.access(workspace, os.W_OK))
    except Exception as e2:
        print('stat error:', e2)
