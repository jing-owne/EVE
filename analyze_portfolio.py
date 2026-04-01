# -*- coding: utf-8 -*-
"""持仓分析脚本 v3 - 通过 ProSearch 获取数据"""
import json
import subprocess
from datetime import datetime

sys = __import__('sys')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ========== 通过 ProSearch 获取股票数据 ==========

def fetch_stock_data_via_prosearch(code, name):
    """通过 ProSearch 获取股票实时数据"""
    try:
        PORT = 19000
        keyword = f'{name} {code} 股票行情 实时价格'
        
        cmd = [
            'curl', '-s', '-X', 'POST',
            f'http://localhost:{PORT}/proxy/prosearch/search',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps({
                "keyword": keyword,
                "mode": 2  # VR卡模式，获取权威数据
            })
        ]
        
        output = subprocess.check_output(cmd, timeout=10).decode('utf-8', errors='replace')
        data = json.loads(output)
        
        if data.get('success'):
            message = data.get('message', '')
            # 从消息中提取价格信息
            # 这是一个简化的解析，实际可能需要更复杂的处理
            return message
        return None
    except Exception as e:
        print(f'ProSearch 查询失败: {e}')
        return None

# ========== 持仓分析 ==========

def analyze_portfolio():
    """分析持仓"""
    portfolio_file = r'C:\Users\admin\.qclaw\workspace\portfolio_config.txt'
    
    holdings = []
    try:
        with open(portfolio_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split(',')
                    if len(parts) >= 3:
                        code = parts[0].strip()
                        name = parts[1].strip()
                        cost = float(parts[2].strip()) if parts[2].strip() else 0
                        qty = float(parts[3].strip()) if len(parts) > 3 and parts[3].strip() else 0
                        
                        holdings.append({
                            'code': code,
                            'name': name,
                            'cost': cost,
                            'qty': qty,
                        })
    except Exception as e:
        print(f'读取持仓配置失败: {e}')
    
    return holdings

# ========== 生成分析报告 ==========

def generate_analysis_report(holdings):
    """生成持仓分析报告"""
    if not holdings:
        return "📊 持仓分析\n\n暂无持仓数据"
    
    report = "📊 **持仓分析** (实时更新)\n\n"
    report += f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for h in holdings:
        report += f"**{h['name']}** ({h['code']})\n"
        
        if h['cost'] > 0 and h['qty'] > 0:
            report += f"  成本价: ¥{h['cost']:.2f} | 持仓: {h['qty']:.0f}股\n"
            report += f"  成本金额: ¥{h['cost'] * h['qty']:.2f}\n"
            report += f"  ⏳ 实时数据获取中...\n"
        else:
            report += f"  ⚠️ 请配置成本价和持仓数量\n"
        
        report += "\n"
    
    report += "---\n"
    report += "💡 **提示**: 请在 portfolio_config.txt 中配置成本价和持仓数量\n"
    report += "格式: 代码,名称,成本价,持仓数量\n"
    report += "例如: 300014,亿纬锂能,25.50,100\n"
    
    return report

# ========== 主程序 ==========

if __name__ == '__main__':
    print('开始分析持仓...')
    holdings = analyze_portfolio()
    
    if holdings:
        report = generate_analysis_report(holdings)
        print('\n' + '='*60)
        print(report)
        print('='*60)
    else:
        print('未获取到持仓数据')
