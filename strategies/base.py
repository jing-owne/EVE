# -*- coding: utf-8 -*-
"""
策略基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from core.data_source import StockData


class BaseStrategy(ABC):
    """策略基类"""

    name: str = "base"
    description: str = ""

    @abstractmethod
    def evaluate(self, stock: StockData) -> float:
        """
        评估股票得分

        Returns:
            0-100分
        """
        pass

    @abstractmethod
    def filter(self, stocks: List[StockData]) -> List[StockData]:
        """过滤股票列表"""
        pass


class MomentumStrategy(BaseStrategy):
    """动量策略"""

    name = "momentum"
    description = "放量上涨 + 均线多头"

    def evaluate(self, stock: StockData) -> float:
        score = 50

        if stock.turnover > 5:
            score += 20
        elif stock.turnover > 3:
            score += 10

        if stock.inflow > 2:
            score += 15
        elif stock.inflow > 0:
            score += 5

        return min(score, 95)

    def filter(self, stocks: List[StockData]) -> List[StockData]:
        return [s for s in stocks if s.turnover >= 3.0 and s.inflow > 0]


class CapitalFlowStrategy(BaseStrategy):
    """资金流向策略"""

    name = "capital_flow"
    description = "主力净流入追踪"

    def evaluate(self, stock: StockData) -> float:
        score = 50

        if stock.inflow >= 5:
            score += 25
        elif stock.inflow >= 2:
            score += 15
        elif stock.inflow >= 1:
            score += 8

        return min(score, 95)

    def filter(self, stocks: List[StockData]) -> List[StockData]:
        return [s for s in stocks if s.inflow >= 1.0]
