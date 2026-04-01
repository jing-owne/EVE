# -*- coding: utf-8 -*-
"""
EVE - A股动量策略引擎主入口
"""

import sys
import argparse
from datetime import datetime

# 修复Windows控制台编码
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 添加项目根目录到路径
sys.path.insert(0, str(__file__).rsplit("eve_main.py", 1)[0])

from core.data_source import DataSource
from core.scanner import Scanner
from core.report import ReportGenerator
from utils.logger import setup_logger
from config.settings import get_config


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="EVE A股动量策略引擎")
    parser.add_argument("--scan", action="store_true", help="执行市场扫描")
    parser.add_argument("--report", action="store_true", help="生成报告")
    parser.add_argument("--output", type=str, default="output/report.html", help="报告输出路径")
    parser.add_argument("--limit", type=int, default=15, help="返回数量")
    parser.add_argument("--debug", action="store_true", help="调试模式")

    args = parser.parse_args()

    # 配置日志
    config = get_config()
    log_level = "DEBUG" if args.debug else config.log_level
    logger = setup_logger(level=log_level)

    logger.info("=" * 50)
    logger.info(f"EVE 启动 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    # 执行扫描
    if args.scan or args.report:
        scanner = Scanner()
        stocks = scanner.scan_all()

        if args.report:
            generator = ReportGenerator()
            html = generator.generate(stocks, limit=args.limit)
            generator.save(html, args.output)
            logger.info(f"报告已生成: {args.output}")

        # 控制台输出
        print(f"\n{'='*50}")
        print(f"📊 Marcus 综合胜率 TOP{args.limit}")
        print(f"{'='*50}\n")

        for i, s in enumerate(stocks[: args.limit], 1):
            medal = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else f"{i:2d}"
            print(f"{medal}. {s.code} {s.name:<8} | 胜率:{s.win_rate:2d}% | {len(s.strategies)}策略 | 涨幅:{s.pct_chg:+.1f}% | 净流入:{s.inflow:.2f}亿")

        print(f"\n{'='*50}")
        print("⚠️ 风险提示: 量化筛选结果，不构成投资建议")
        print(f"{'='*50}\n")

    logger.info("完成")


if __name__ == "__main__":
    main()
