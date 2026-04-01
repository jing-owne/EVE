# -*- coding: utf-8 -*-
"""
EVE - A股动量策略引擎
"""

__version__ = "2.0.0"
__author__ = "Marcus"

from core.data_source import DataSource
from core.scanner import Scanner
from core.report import ReportGenerator

__all__ = ["DataSource", "Scanner", "ReportGenerator"]
