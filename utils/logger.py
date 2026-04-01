# -*- coding: utf-8 -*-
"""
日志系统
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(
    name: str = "eve",
    level: str = "INFO",
    log_file: bool = True,
    log_dir: str = "logs"
) -> logging.Logger:
    """
    配置日志器

    Args:
        name: 日志器名称
        level: 日志级别
        log_file: 是否输出到文件
        log_dir: 日志目录
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 格式
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 控制台输出
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # 文件输出
    if log_file:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        file_handler = logging.FileHandler(
            log_path / f"{today}.log",
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger
