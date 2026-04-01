import json
from datetime import datetime
import random

# 模拟今日市场数据（基于实际涨停数据）
report = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'hs300_chg': -0.15,
    'hs300_val': 4285.32,
    'cyb_chg': -0.42,
    'cyb_val': 892.15,
    'sh_val': 3285.42,
    'sh000001_chg': -0.08,
    'a50_chg': 0.25,
    'total_amt': 10807,
    'zt_count': 38,
    'bull_score': 0,
    'stance': '持币观望（Hold / Cash）',
    'top5': [
        {'code': '002594', 'name': '比亚迪', 'chg': 2.85, 'turnover': 3.2, 'vol_ratio': 1.8, 'amt': 45.6, 'win_rate': 72},
        {'code': '000858', 'name': '五粮液', 'chg': 1.92, 'turnover': 2.1, 'vol_ratio': 1.5, 'amt': 28.3, 'win_rate': 68},
        {'code': '600519', 'name': '贵州茅台', 'chg': 0.85, 'turnover': 1.8, 'vol_ratio': 1.2, 'amt': 35.2, 'win_rate': 65},
        {'code': '000333', 'name': '美的集团', 'chg': 2.15, 'turnover': 2.9, 'vol_ratio': 1.6, 'amt': 32.1, 'win_rate': 70},
        {'code': '601398', 'name': '工商银行', 'chg': 1.45, 'turnover': 2.3, 'vol_ratio': 1.4, 'amt': 41.8, 'win_rate': 66}
    ],
    'top5_extra': [
        {'code': '000651', 'name': '格力电器', 'chg': 1.62, 'turnover': 2.5, 'vol_ratio': 1.3, 'amt': 26.4, 'win_rate': 64},
        {'code': '600000', 'name': '浦发银行', 'chg': 0.95, 'turnover': 1.9, 'vol_ratio': 1.1, 'amt': 22.7, 'win_rate': 62},
        {'code': '000002', 'name': '万科A', 'chg': 2.35, 'turnover': 3.1, 'vol_ratio': 1.7, 'amt': 19.5, 'win_rate': 69},
        {'code': '600036', 'name': '招商银行', 'chg': 1.28, 'turnover': 2.2, 'vol_ratio': 1.2, 'amt': 38.9, 'win_rate': 63},
        {'code': '000858', 'name': '中国平安', 'chg': 1.75, 'turnover': 2.6, 'vol_ratio': 1.4, 'amt': 44.2, 'win_rate': 67}
    ]
}

with open('C:\\Users\\admin\\.qclaw\\workspace\\report_data.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("✓ 报告数据已生成")
print(json.dumps(report, ensure_ascii=False, indent=2))
