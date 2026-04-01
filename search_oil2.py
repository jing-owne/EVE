import urllib.request
import json
import time

PORT = 19000
FROM_TIME = int(time.time()) - 2592000
keyword = "2026年3月中国汽油价格调整 92号95号98号"

body = json.dumps({"keyword": keyword, "from_time": FROM_TIME}).encode("utf-8")
req = urllib.request.Request(
    f"http://localhost:{PORT}/proxy/prosearch/search",
    data=body,
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=20) as resp:
    result = resp.read().decode("utf-8")
    with open(r"C:\Users\admin\.qclaw\workspace\oil_result.txt", "w", encoding="utf-8") as f:
        f.write(result)
    print("Done")
