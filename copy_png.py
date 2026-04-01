import shutil, os

src = 'C:/Users/admin/.qclaw/workspace/marcus_report.png'
dst = 'C:/Users/admin/.qclaw/workspace/marcus_report_copy.png'

try:
    # Read existing file
    with open(src, 'rb') as f:
        data = f.read()
    print('Read OK, size:', len(data))
    
    # Write to new file
    with open(dst, 'wb') as f:
        f.write(data)
    print('Write OK:', dst)
    
    # Verify
    size = os.path.getsize(dst)
    print('File size:', size)
    
except Exception as e:
    print('ERROR:', e)
