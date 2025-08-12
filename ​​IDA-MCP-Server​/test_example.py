"""
测试示例文件 - 用于验证代码分析功能
"""

import os
import sys
import json


def complex_function(data, options=None):
    """一个复杂度较高的函数示例"""
    if not data:
        return None
    
    if options is None:
        options = {}
    
    result = []
    
    for item in data:
        if isinstance(item, dict):
            if 'type' in item:
                if item['type'] == 'A':
                    if 'value' in item:
                        if item['value'] > 0:
                            result.append(item['value'] * 2)
                        else:
                            result.append(0)
                    else:
                        result.append(1)
                elif item['type'] == 'B':
                    if 'value' in item:
                        result.append(item['value'] + 10)
                    else:
                        result.append(10)
                else:
                    result.append(-1)
            else:
                result.append(0)
        elif isinstance(item, (int, float)):
            if item > 100:
                result.append(item / 2)
            elif item > 50:
                result.append(item * 1.5)
            elif item > 0:
                result.append(item)
            else:
                result.append(0)
        else:
            try:
                converted = float(item)
                result.append(converted)
            except (ValueError, TypeError):
                result.append(0)
    
    # 这行代码太长了，超过了120个字符的限制，这是一个代码风格问题的示例，应该被检测出来并给出警告
    
    if options.get('sort', False):
        result.sort()
    
    if options.get('unique', False):
        result = list(set(result))
    
    return result


class DataProcessor:
    """数据处理器类"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.processed_count = 0
    
    def process(self, data):
        """处理数据"""
        if not data:
            return []
        
        processed = []
        for item in data:
            processed_item = self._process_item(item)
            if processed_item is not None:
                processed.append(processed_item)
        
        self.processed_count += len(processed)
        return processed
    
    def _process_item(self, item):
        """处理单个数据项"""
        if isinstance(item, str):
            return item.strip().lower()
        elif isinstance(item, (int, float)):
            return item * self.config.get('multiplier', 1)
        else:
            return str(item)


# 一些未使用的导入示例
import datetime
import re
import urllib.parse
import hashlib
import base64
import uuid
import random
import math
import collections
import itertools
import functools
import operator
import pickle
import csv
import xml.etree.ElementTree
import sqlite3
import threading
import multiprocessing


def simple_function(x, y):
    """简单函数示例"""
    return x + y


if __name__ == "__main__":
    # 测试代码
    test_data = [1, 2, 3, {'type': 'A', 'value': 5}]
    processor = DataProcessor({'multiplier': 2})
    result = processor.process(test_data)
    print(f"处理结果: {result}")