# -*- coding: utf-8 -*-
"""
市场扫描引擎
整合多策略选股逻辑
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

from core.data_source import StockData, DataSource

logger = logging.getLogger(__name__)


@dataclass
class ScanResult:
    """扫描结果"""
    code: str
    name: str
    win_rate: int
    strategies: List[str]
    pct_chg: float
    amount: float
    turnover: float
    inflow: float
    signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "win_rate": self.win_rate,
            "strategies": self.strategies,
            "pct_chg": self.pct_chg,
            "amount": self.amount,
            "turnover": self.turnover,
            "inflow": self.inflow,
            "signal": self.signal,
        }


class Scanner:
    """市场扫描器"""

    # 筛选条件
    MIN_TURNOVER = 1.0  # 最小换手率
    MIN_AMOUNT = 0.2    # 最小成交额（亿）
    MAX_PCT_CHG = 9.5   # 最大涨幅（排除涨停）

    def __init__(self, data_source: Optional[DataSource] = None):
        self.data = data_source or DataSource()

    def _filter_liquid(self, stocks: List[StockData]) -> List[StockData]:
        """流动性过滤"""
        return [
            s for s in stocks
            if s.turnover >= self.MIN_TURNOVER and s.amount >= self.MIN_AMOUNT
        ]

    def _calc_win_rate(self, stock: StockData, strategy_hits: int) -> int:
        """
        计算胜率

        规则:
        - 基础胜率 50%
        - 每命中一个策略 +10%
        - 主力净流入加分
        - 换手率加分
        - 涨幅在合理区间加分
        """
        base = 50 + strategy_hits * 10

        # 主力净流入加分
        if stock.inflow >= 5:
            base += 15
        elif stock.inflow >= 2:
            base += 10
        elif stock.inflow >= 1:
            base += 5

        # 换手率加分
        if 3 <= stock.turnover <= 8:
            base += 10  # 温和放量最佳
        elif stock.turnover > 8:
            base += 5   # 过量需谨慎

        # 涨幅在合理区间
        if 0 < stock.pct_chg <= 5:
            base += 5

        return min(base, 97)

    def _get_signal(self, stock: StockData) -> str:
        """生成信号"""
        if stock.pct_chg > 3:
            return "强势整理"
        elif stock.pct_chg < -2:
            return "超跌关注"
        elif stock.turnover > 5 and stock.inflow > 0:
            return "资金活跃"
        elif stock.pct_chg > 0 and stock.inflow > 0:
            return "量价齐升"
        else:
            return "观察"

    def scan_all(self) -> List[ScanResult]:
        """
        综合扫描

        整合五大策略:
        1. 放量上涨（换手率排序）
        2. 成交额排名
        3. 多因子量化（涨幅+成交额）
        4. AI技术面（主力净流入）
        5. 目标价+机构
        """
        # 获取各类排行
        by_turnover = self._filter_liquid(self.data.get_stocks_by_turnover(100))
        by_amount = self._filter_liquid(self.data.get_stocks_by_amount(100))
        by_pct_chg = self._filter_liquid(self.data.get_top_gainers(3.0, 2.0))
        by_inflow = self.data.get_top_inflow(0.5)
        by_inflow_strong = self.data.get_top_inflow(1.0)

        # 去重并统计命中次数
        all_stocks: Dict[str, Dict[str, Any]] = {}

        for stock in by_turnover[:50]:
            if stock.code not in all_stocks:
                all_stocks[stock.code] = {"stock": stock, "strategies": []}
            all_stocks[stock.code]["strategies"].append("放量上涨")

        for stock in by_amount[:50]:
            if stock.code not in all_stocks:
                all_stocks[stock.code] = {"stock": stock, "strategies": []}
            all_stocks[stock.code]["strategies"].append("成交额")

        for stock in by_pct_chg[:50]:
            if stock.code not in all_stocks:
                all_stocks[stock.code] = {"stock": stock, "strategies": []}
            all_stocks[stock.code]["strategies"].append("多因子")

        for stock in by_inflow[:50]:
            if stock.code not in all_stocks:
                all_stocks[stock.code] = {"stock": stock, "strategies": []}
            all_stocks[stock.code]["strategies"].append("技术面")

        for stock in by_inflow_strong[:50]:
            if stock.code not in all_stocks:
                all_stocks[stock.code] = {"stock": stock, "strategies": []}
            all_stocks[stock.code]["strategies"].append("机构")

        # 生成结果
        results = []
        for code, info in all_stocks.items():
            stock = info["stock"]
            strategies = list(set(info["strategies"]))

            result = ScanResult(
                code=code,
                name=stock.name,
                win_rate=self._calc_win_rate(stock, len(strategies)),
                strategies=strategies,
                pct_chg=stock.pct_chg,
                amount=stock.amount,
                turnover=stock.turnover,
                inflow=stock.inflow,
                signal=self._get_signal(stock),
            )
            results.append(result)

        # 按胜率排序
        results.sort(key=lambda x: x.win_rate, reverse=True)

        logger.info(f"扫描完成: {len(results)} 只标的")
        return results

    def get_top_picks(self, limit: int = 15) -> List[ScanResult]:
        """获取推荐标的"""
        results = self.scan_all()
        return results[:limit]

    def get_short_term_plays(self, limit: int = 15) -> List[ScanResult]:
        """短线机会（高涨幅+高换手）"""
        results = self.scan_all()
        short_term = [
            r for r in results
            if r.pct_chg >= 5.0 and r.turnover >= 3.0
        ]
        return short_term[:limit]
