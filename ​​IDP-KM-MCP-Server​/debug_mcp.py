#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP服务器调试脚本
"""

import os
import sys
import traceback
import sqlite3
from pathlib import Path

def check_dependencies():
    """检查依赖项"""
    print("=== 检查依赖项 ===")
    
    # 检查基础依赖
    try:
        from mcp.server.fastmcp import FastMCP
        print("✓ FastMCP 导入成功")
    except ImportError as e:
        print(f"✗ FastMCP 导入失败: {e}")
        return False
    
    # 检查可选依赖
    try:
        import PyPDF2
        print("✓ PyPDF2 可用")
    except ImportError:
        print("⚠ PyPDF2 不可用 (PDF处理将被禁用)")
    
    try:
        from docx import Document
        print("✓ python-docx 可用")
    except ImportError:
        print("⚠ python-docx 不可用 (DOCX处理将被禁用)")
    
    try:
        import jieba
        print("✓ jieba 可用")
    except ImportError:
        print("⚠ jieba 不可用 (中文分词将被禁用)")
    
    return True

def check_database():
    """检查数据库"""
    print("\n=== 检查数据库 ===")
    
    db_path = "documents.db"
    
    try:
        # 检查数据库文件
        if os.path.exists(db_path):
            print(f"✓ 数据库文件存在: {db_path}")
            print(f"  文件大小: {os.path.getsize(db_path)} bytes")
        else:
            print(f"⚠ 数据库文件不存在，将创建: {db_path}")
        
        # 测试数据库连接
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表结构
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✓ 数据库连接成功，表数量: {len(tables)}")
        
        for table in tables:
            print(f"  - {table[0]}")
        
        # 检查数据
        cursor.execute("SELECT COUNT(*) FROM documents")
        doc_count = cursor.fetchone()[0]
        print(f"  文档数量: {doc_count}")
        
        cursor.execute("SELECT COUNT(*) FROM knowledge_base")
        kb_count = cursor.fetchone()[0]
        print(f"  知识库条目数量: {kb_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ 数据库检查失败: {e}")
        traceback.print_exc()
        return False

def test_document_parsing():
    """测试文档解析"""
    print("\n=== 测试文档解析 ===")
    
    # 测试文件路径
    test_file = "docs/金发科技stock_analysis_sse_600143_20250811T024734.md"
    
    if not os.path.exists(test_file):
        print(f"✗ 测试文件不存在: {test_file}")
        return False
    
    print(f"✓ 测试文件存在: {test_file}")
    print(f"  文件大小: {os.path.getsize(test_file)} bytes")
    
    try:
        # 测试文件读取
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✓ 文件读取成功，内容长度: {len(content)} 字符")
        
        # 测试哈希计算
        import hashlib
        hash_md5 = hashlib.md5()
        with open(test_file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        file_hash = hash_md5.hexdigest()
        print(f"✓ 文件哈希计算成功: {file_hash[:16]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ 文档解析测试失败: {e}")
        traceback.print_exc()
        return False

def test_mcp_server():
    """测试MCP服务器初始化"""
    print("\n=== 测试MCP服务器 ===")
    
    try:
        from mcp.server.fastmcp import FastMCP
        
        # 创建服务器实例
        mcp = FastMCP("DocumentProcessor")
        print("✓ MCP服务器实例创建成功")
        
        # 测试工具注册
        @mcp.tool()
        def test_tool() -> str:
            """测试工具"""
            return "测试成功"
        
        print("✓ 工具注册成功")
        
        return True
        
    except Exception as e:
        print(f"✗ MCP服务器测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("MCP服务器调试开始...")
    print(f"Python版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    
    success = True
    
    # 检查各个组件
    success &= check_dependencies()
    success &= check_database()
    success &= test_document_parsing()
    success &= test_mcp_server()
    
    print(f"\n=== 调试结果 ===")
    if success:
        print("✓ 所有检查通过，MCP服务器应该可以正常运行")
    else:
        print("✗ 发现问题，请根据上述信息修复")
    
    return success

if __name__ == "__main__":
    main()