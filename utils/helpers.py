# -*- coding: utf-8 -*-
"""
工具函数
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


def ensure_dir(path: str) -> Path:
    """确保目录存在"""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def load_json(path: str, default: Any = None) -> Any:
    """加载JSON文件"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        return default


def save_json(path: str, data: Any, indent: int = 2) -> None:
    """保存JSON文件"""
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def safe_float(value: Any, default: float = 0.0) -> float:
    """安全转换为float"""
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default
