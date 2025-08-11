"""
MCP服务器配置文件
"""

import os
from pathlib import Path

# 数据库配置
DATABASE_CONFIG = {
    "path": "documents.db",
    "timeout": 30.0,
    "check_same_thread": False
}

# 文档处理配置
DOCUMENT_CONFIG = {
    "max_file_size": 50 * 1024 * 1024,  # 50MB
    "supported_extensions": [".txt", ".pdf", ".docx", ".doc"],
    "encoding_fallbacks": ["utf-8", "gbk", "gb2312", "latin-1"],
    "max_keywords": 20,
    "max_summary_sentences": 5
}

# 服务器配置
SERVER_CONFIG = {
    "name": "DocumentProcessor",
    "version": "1.0.0",
    "description": "智能文档处理与知识管理MCP服务器",
    "transport": "stdio"  # 可选: stdio, sse
}

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "mcp_server.log"
}

# 功能开关
FEATURES = {
    "pdf_processing": True,
    "docx_processing": True,
    "chinese_processing": True,
    "auto_summary": True,
    "auto_keywords": True,
    "file_deduplication": True
}

# 路径配置
PATHS = {
    "data_dir": Path("data"),
    "logs_dir": Path("logs"),
    "temp_dir": Path("temp")
}

# 确保目录存在
for path in PATHS.values():
    path.mkdir(exist_ok=True)

def get_config(section: str = None):
    """获取配置"""
    if section == "database":
        return DATABASE_CONFIG
    elif section == "document":
        return DOCUMENT_CONFIG
    elif section == "server":
        return SERVER_CONFIG
    elif section == "logging":
        return LOGGING_CONFIG
    elif section == "features":
        return FEATURES
    elif section == "paths":
        return PATHS
    else:
        return {
            "database": DATABASE_CONFIG,
            "document": DOCUMENT_CONFIG,
            "server": SERVER_CONFIG,
            "logging": LOGGING_CONFIG,
            "features": FEATURES,
            "paths": PATHS
        }