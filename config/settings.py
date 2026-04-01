# -*- coding: utf-8 -*-
"""
配置管理模块
"""

import os
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EmailConfig:
    """邮件配置"""
    host: str = "smtp.qq.com"
    port: int = 465
    user: str = ""
    password: str = ""
    from_name: str = "Marcus"
    to_email: str = ""
    cc_emails: str = ""


@dataclass
class ScanConfig:
    """扫描配置"""
    min_turnover: float = 1.0
    min_amount: float = 0.2
    max_pct_chg: float = 9.5
    top_limit: int = 15
    exclude_prefixes: list = field(default_factory=lambda: ["688", "8", "4"])


@dataclass
class Config:
    """全局配置"""
    email: EmailConfig = field(default_factory=EmailConfig)
    scan: ScanConfig = field(default_factory=ScanConfig)
    debug: bool = False
    log_level: str = "INFO"

    @classmethod
    def load(cls, path: Optional[str] = None) -> "Config":
        """加载配置"""
        config = cls()

        # 尝试加载YAML配置
        if path is None:
            path = os.environ.get(
                "EVE_CONFIG",
                str(Path(__file__).parent.parent / "config" / "settings.yaml")
            )

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            # 解析邮件配置
            if "email" in data:
                for k, v in data["email"].items():
                    if hasattr(config.email, k):
                        setattr(config.email, k, v)

            # 解析扫描配置
            if "scan" in data:
                for k, v in data["scan"].items():
                    if hasattr(config.scan, k):
                        setattr(config.scan, k, v)

            # 其他配置
            if "debug" in data:
                config.debug = data["debug"]
            if "log_level" in data:
                config.log_level = data["log_level"]

        # 环境变量覆盖
        if os.environ.get("DEBUG_MODE", "").lower() == "true":
            config.debug = True

        return config


# 全局配置实例
_config: Optional[Config] = None


def get_config() -> Config:
    """获取配置实例"""
    global _config
    if _config is None:
        _config = Config.load()
    return _config
