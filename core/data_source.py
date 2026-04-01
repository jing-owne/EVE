# -*- coding: utf-8 -*-
"""
数据源抽象层
统一管理所有数据获取接口
"""

import json
import urllib.request
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class StockData:
    """股票数据结构"""
    code: str
    name: str
    price: float
    prev_close: float
    pct_chg: float
    amount: float  # 成交额（亿）
    turnover: float  # 换手率
    volume: float  # 成交量
    inflow: float  # 主力净流入（亿）

    @property
    def is_up(self) -> bool:
        return self.pct_chg > 0

    @property
    def is_limit_up(self) -> bool:
        return self.pct_chg >= 9.8

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "price": self.price,
            "pct_chg": self.pct_chg,
            "amount": self.amount,
            "turnover": self.turnover,
            "inflow": self.inflow,
        }


class BaseDataSource(ABC):
    """数据源基类"""

    @abstractmethod
    def get_realtime_data(self, codes: List[str]) -> List[StockData]:
        """获取实时数据"""
        pass

    @abstractmethod
    def get_market_rank(self, sort_by: str, limit: int = 100) -> List[StockData]:
        """获取市场排名"""
        pass

    @abstractmethod
    def get_index_data(self) -> Dict[str, Any]:
        """获取指数数据"""
        pass


class EastMoneySource(BaseDataSource):
    """东方财富数据源"""

    BASE_URL = "https://push2.eastmoney.com/api/qt/clist/get"

    # 字段映射: f2=价格, f3=涨幅, f5=成交量, f6=成交额, f8=换手率, f12=代码, f14=名称, f62=主力净流入
    FIELDS = "f2,f3,f5,f6,f7,f8,f10,f12,f14,f62"

    # 市场筛选: m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23
    MARKET_FILTER = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://finance.eastmoney.com/",
    }

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def _fetch(self, url: str) -> Dict:
        """统一请求方法"""
        try:
            req = urllib.request.Request(url, headers=self.HEADERS)
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace").strip()
                if raw.startswith("jQuery"):
                    raw = raw[raw.index("(") + 1 : raw.rindex(")")]
                return json.loads(raw)
        except Exception as e:
            logger.error(f"请求失败: {e}")
            return {}

    def _build_url(self, fid: str, pz: int = 100) -> str:
        """构建请求URL"""
        return (
            f"{self.BASE_URL}?pn=1&pz={pz}&po=1&np=1&fltt=2&invt=2&fid={fid}"
            f"&fs={self.MARKET_FILTER}&fields={self.FIELDS}&_={int(time.time()*1000)}"
        )

    def _parse_stock(self, item: Dict) -> Optional[StockData]:
        """解析单只股票数据"""
        code = str(item.get("f12", ""))
        if not code or code.startswith("688") or code.startswith("8") or code.startswith("4"):
            return None

        try:
            price = float(item.get("f2", 0) or 0)
            prev_close = price / (1 + item.get("f3", 0) / 1000) if price > 0 else 0
            pct_chg = item.get("f3", 0) / 10
            amount = item.get("f6", 0) / 1e8
            turnover = item.get("f8", 0) / 10
            inflow = item.get("f62", 0) / 1e8

            return StockData(
                code=code,
                name=item.get("f14", "?"),
                price=price,
                prev_close=prev_close,
                pct_chg=pct_chg,
                amount=amount,
                turnover=turnover,
                volume=item.get("f5", 0),
                inflow=inflow,
            )
        except Exception as e:
            logger.warning(f"解析失败 {code}: {e}")
            return None

    def get_realtime_data(self, codes: List[str]) -> List[StockData]:
        """获取实时数据（暂未实现批量查询）"""
        # 东方财富不支持批量查询，需要单独实现或使用腾讯接口
        logger.warning("realtime_data 暂未实现，使用 market_rank 替代")
        return []

    def get_market_rank(self, sort_by: str = "f3", limit: int = 100) -> List[StockData]:
        """
        获取市场排名

        Args:
            sort_by: 排序字段 f3=涨幅, f6=成交额, f8=换手率, f62=主力净流入
            limit: 返回数量
        """
        url = self._build_url(sort_by, limit)
        data = self._fetch(url)

        results = []
        diff = data.get("data", {}).get("diff", [])

        for item in diff:
            stock = self._parse_stock(item)
            if stock:
                results.append(stock)

        logger.info(f"获取市场排名 {sort_by}: {len(results)} 只")
        return results

    def get_index_data(self) -> Dict[str, Any]:
        """获取指数数据"""
        # 简化实现，后续可扩展
        return {
            "timestamp": datetime.now().isoformat(),
            "indices": {},
        }


class DataSource:
    """数据源管理器"""

    def __init__(self, source: str = "eastmoney"):
        self._source = EastMoneySource() if source == "eastmoney" else None

    def get_stocks_by_turnover(self, limit: int = 100) -> List[StockData]:
        """按换手率排序"""
        return self._source.get_market_rank("f8", limit)

    def get_stocks_by_amount(self, limit: int = 100) -> List[StockData]:
        """按成交额排序"""
        return self._source.get_market_rank("f6", limit)

    def get_stocks_by_pct_chg(self, limit: int = 200) -> List[StockData]:
        """按涨幅排序"""
        return self._source.get_market_rank("f3", limit)

    def get_stocks_by_inflow(self, limit: int = 100) -> List[StockData]:
        """按主力净流入排序"""
        return self._source.get_market_rank("f62", limit)

    def get_top_gainers(self, min_pct: float = 3.0, min_amount: float = 2.0) -> List[StockData]:
        """获取涨幅榜（过滤条件）"""
        stocks = self.get_stocks_by_pct_chg(200)
        return [s for s in stocks if s.pct_chg >= min_pct and s.amount >= min_amount]

    def get_top_inflow(self, min_inflow: float = 1.0) -> List[StockData]:
        """获取主力净流入榜（过滤条件）"""
        stocks = self.get_stocks_by_inflow(100)
        return [s for s in stocks if s.inflow >= min_inflow]
