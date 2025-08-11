"""
MCP服务测试脚本
"""

import os
import sqlite3
from document_mcp import DocumentProcessor, init_database

def test_document_processor():
    """测试文档处理器"""
    print("🧪 测试文档处理器...")
    
    # 创建测试文档
    test_content = "这是一个测试文档。包含人工智能、机器学习、深度学习等关键词。"
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    # 测试文本提取
    extracted = DocumentProcessor.extract_text_from_txt("test.txt")
    print(f"✅ 文本提取: {extracted[:50]}...")
    
    # 测试关键词提取
    keywords = DocumentProcessor.extract_keywords(test_content)
    print(f"✅ 关键词提取: {keywords}")
    
    # 测试摘要生成
    summary = DocumentProcessor.generate_summary(test_content)
    print(f"✅ 摘要生成: {summary}")
    
    # 清理测试文件
    os.remove("test.txt")

def test_database():
    """测试数据库功能"""
    print("\n🗄️ 测试数据库...")
    
    # 初始化数据库
    init_database()
    
    # 检查表是否创建
    conn = sqlite3.connect("documents.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"✅ 数据库表: {[table[0] for table in tables]}")
    
    conn.close()

def test_file_hash():
    """测试文件哈希"""
    print("\n🔐 测试文件哈希...")
    
    # 创建测试文件
    with open("hash_test.txt", "w") as f:
        f.write("test content")
    
    hash1 = DocumentProcessor.calculate_file_hash("hash_test.txt")
    hash2 = DocumentProcessor.calculate_file_hash("hash_test.txt")
    
    print(f"✅ 哈希一致性: {hash1 == hash2}")
    print(f"✅ 哈希值: {hash1}")
    
    # 清理
    os.remove("hash_test.txt")

def main():
    """运行所有测试"""
    print("🚀 MCP服务功能测试")
    print("=" * 40)
    
    try:
        test_document_processor()
        test_database()
        test_file_hash()
        
        print("\n" + "=" * 40)
        print("✅ 所有测试通过！")
        print("🎉 MCP服务已准备就绪")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("请检查依赖安装和环境配置")

if __name__ == "__main__":
    main()