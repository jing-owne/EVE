# -*- coding: utf-8 -*-
"""
测试扫描器
"""

import pytest
from core.scanner import Scanner


def test_scanner():
    """测试扫描器"""
    scanner = Scanner()
    results = scanner.scan_all()

    assert isinstance(results, list)
    assert len(results) > 0

    # 检查胜率范围
    for r in results:
        assert 50 <= r.win_rate <= 97
        assert len(r.strategies) >= 1


def test_top_picks():
    """测试推荐标的"""
    scanner = Scanner()
    top = scanner.get_top_picks(limit=10)

    assert len(top) == 10
    assert top[0].win_rate >= top[-1].win_rate  # 降序排列


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
