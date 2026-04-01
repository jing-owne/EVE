# -*- coding: utf-8 -*-
"""
报告生成器
生成HTML邮件报告
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from core.scanner import ScanResult

logger = logging.getLogger(__name__)


class ReportGenerator:
    """报告生成器"""

    def __init__(self):
        self.timestamp = datetime.now()

    def _get_day_name(self) -> str:
        """获取星期几"""
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return days[self.timestamp.weekday()]

    def _build_table(self, title: str, stocks: List[ScanResult], limit: int = 10) -> str:
        """构建数据表格"""
        rows = ""
        for i, s in enumerate(stocks[:limit]):
            pct_str = f'<span style="color:#e94560">{s.pct_chg:+.1f}%</span>' if s.pct_chg > 0 else f'<span style="color:#27ae60">{s.pct_chg:+.1f}%</span>'
            inflow_str = f'<span style="color:#e94560">{s.inflow:.2f}亿</span>' if s.inflow > 0 else f'<span style="color:#27ae60">{s.inflow:.2f}亿</span>'

            row_class = "highlight" if i < 3 else ""
            rows += f'''<tr class="{row_class}">
  <td>{i+1}</td>
  <td>{s.code}</td>
  <td><b>{s.name}</b></td>
  <td>{pct_str}</td>
  <td>{s.amount:.1f}亿</td>
  <td>{s.turnover:.2f}%</td>
  <td>{inflow_str}</td>
</tr>'''

        if not stocks:
            rows = '<tr><td colspan="7" style="text-align:center;color:#aaa;padding:16px;">📭 当前暂无符合标的</td></tr>'

        return f'''
<h2 style="color:#1a1a2e;margin:20px 0 10px 0;font-size:16px;border-left:4px solid #e94560;padding-left:10px;">{title}</h2>
<table class="data-table">
  <thead><tr><th>排名</th><th>代码</th><th>名称</th><th>涨跌幅</th><th>成交额</th><th>换手率</th><th>主力净流入</th></tr></thead>
  <tbody>{rows}</tbody>
</table>'''

    def _build_rank_table(self, stocks: List[ScanResult], limit: int = 15) -> str:
        """构建胜率排行表"""
        rows = ""
        medals = ["🥇", "🥈", "🥉"]

        for i, s in enumerate(stocks[:limit]):
            medal = medals[i] if i < 3 else f"{i+1}"
            bg = "#fff3cd" if i < 3 else ("#fafafa" if i % 2 == 0 else "#fff")

            rows += f'''<tr style="background:{bg}">
  <td><b>{medal}</b></td>
  <td>{s.code}</td>
  <td><b>{s.name}</b></td>
  <td><span style="color:#e94560;font-weight:bold">{s.win_rate}%</span></td>
  <td>{len(s.strategies)}策略</td>
  <td><span style="color:{"#e94560" if s.pct_chg>0 else "#27ae60"}">{s.pct_chg:+.1f}%</span></td>
  <td><span style="color:{"#e94560" if s.inflow>0 else "#27ae60"}">{s.inflow:.2f}亿</span></td>
  <td>{s.turnover:.2f}%</td>
</tr>'''

        return f'''
<h1 style="color:#fff;background:linear-gradient(135deg,#e94560,#1a1a2e);margin:20px 0 10px 0;font-size:18px;font-weight:bold;padding:12px 18px;border-radius:8px;">🏆 综合胜率 TOP{limit}</h1>
<table class="data-table rank-table">
  <thead><tr><th>排名</th><th>代码</th><th>名称</th><th>综合胜率</th><th>策略命中</th><th>涨跌幅</th><th>主力净流入</th><th>换手率</th></tr></thead>
  <tbody>{rows}</tbody>
</table>'''

    def generate(self, stocks: List[ScanResult], limit: int = 15) -> str:
        """
        生成HTML报告

        Args:
            stocks: 扫描结果列表
            limit: 显示数量
        """
        day_name = self._get_day_name()
        date_str = self.timestamp.strftime("%Y-%m-%d")
        time_str = self.timestamp.strftime("%H:%M:%S")

        # 按策略分组
        high_turnover = sorted(stocks, key=lambda x: x.turnover, reverse=True)[:10]
        high_amount = sorted(stocks, key=lambda x: x.amount, reverse=True)[:10]
        high_pct = sorted(stocks, key=lambda x: x.pct_chg, reverse=True)[:10]
        high_inflow = sorted(stocks, key=lambda x: x.inflow, reverse=True)[:10]

        html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  body {{ font-family:"Microsoft YaHei","PingFang SC",sans-serif; background:#f4f6f9; margin:0; padding:15px; }}
  .container {{ max-width:900px; margin:0 auto; background:#fff; border-radius:12px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08); }}
  .header {{ background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%); color:#fff; padding:25px 30px; }}
  .header h1 {{ margin:0 0 5px 0; font-size:20px; }}
  .header p {{ margin:0; font-size:13px; color:#aab; }}
  .data-table {{ width:100%; border-collapse:collapse; font-size:13px; margin-bottom:20px; }}
  .data-table th {{ background:#1a1a2e; color:#fff; padding:8px 10px; text-align:left; font-weight:normal; }}
  .data-table td {{ padding:7px 10px; border-bottom:1px solid #eee; }}
  .data-table tr:hover {{ background:#f8f9fa; }}
  .data-table tr.highlight {{ background:#fff9f0; }}
  .footer {{ background:#f8f9fa; padding:15px 25px; font-size:12px; color:#888; text-align:center; border-top:1px solid #eee; }}
</style></head><body>
<div class="container">
  <div class="header">
    <h1>📊 Marcus A股动量策略报告</h1>
    <p>{date_str}（{day_name}）| 数据来源：东方财富 | 排除688/北交所</p>
  </div>
  <div style="padding:20px 25px">
    {self._build_rank_table(stocks, limit)}
    {self._build_table("策略① 放量上涨（换手率排序）", high_turnover)}
    {self._build_table("策略② 成交额排名", high_amount)}
    {self._build_table("策略③ 多因子量化（涨幅排序）", high_pct)}
    {self._build_table("策略④ AI技术面（主力净流入排序）", high_inflow)}
    <div style="background:#f0f8f0;padding:14px 16px;border-radius:6px;font-size:13px;line-height:1.8;margin-top:20px;">
      <p><b style="color:#27ae60">📈 操作建议：</b></p>
      <ul style="margin:5px 0;padding-left:20px;">
        <li>综合胜率≥70%的标的，可在支撑位布局</li>
        <li>止损原则：<b style="color:#e94560">-3%无条件出场</b></li>
      </ul>
    </div>
  </div>
  <div class="footer">
    <p>📊 Marcus | 高级日内动量策略师</p>
    <p>⚠️ 免责声明：本报告仅为数据扫描结果，不构成投资建议。生成时间：{time_str}</p>
  </div>
</div></body></html>'''

        return html

    def save(self, html: str, filepath: str) -> None:
        """保存报告"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        logger.info(f"报告已保存: {filepath}")
