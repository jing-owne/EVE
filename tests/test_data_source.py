# -*- coding: utf-8 -*-
"""
测试数据源
"""

import pytest
from core.data_source import DataSource, StockData


def test_stock_data_creation():
    """测试股票数据创建"""
    stock = StockData(
        code="000001",
        name="平安银行",
        price=10.5,
        prev_close=10.0,
        pct_chg=5.0,
        amount=10.0,
        turnover=3.5,
        volume=1000000,
        inflow=2.5,
    )

    assert stock.code == "000001"
    assert stock.is_up is True
    assert stock.is_limit_up is False


def test_data_source():
    """测试数据源"""
    source = DataSource()
    stocks = source.get_stocks_by_pct_chg(limit=50)

    assert isinstance(stocks, list)
    assert len(stocks) > 0

    # 检查字段
    for s in stocks:
        assert s.code is not None
        assert s.name is not None
        assert not s.code.startswith("688")  # 排除科创板


def test_top_gainers():
    """测试涨幅榜"""
    source = DataSource()
    stocks = source.get_top_gainers(min_pct=3.0, min_amount=2.0)

    for s in stocks:
        assert s.pct_chg >= 3.0
        assert s.amount >= 2.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
