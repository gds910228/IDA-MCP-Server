"""
智能文档处理与知识管理MCP - 使用示例
"""

import os
import json

def create_sample_documents():
    """创建示例文档"""
    
    # 创建AI报告示例
    ai_content = """人工智能技术发展报告

人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。
近年来，机器学习、深度学习和自然语言处理等技术取得了显著进展。

主要应用领域包括：
1. 自然语言处理
2. 计算机视觉  
3. 机器人技术
4. 专家系统

未来发展趋势：
- 更强的通用人工智能
- 更好的人机交互
- 更广泛的应用场景

关键技术：
深度学习、神经网络、机器学习、自然语言处理、计算机视觉等技术正在推动AI的快速发展。
"""
    
    # 创建技术文档示例
    tech_content = """MCP协议技术文档

Model Context Protocol (MCP) 是一个开放标准，用于连接AI助手与各种数据源和工具。

核心特性：
- 标准化接口
- 工具集成
- 资源访问
- 安全通信

实现方式：
1. 服务器端实现
2. 客户端连接
3. 协议通信
4. 数据交换

应用场景：
MCP协议广泛应用于AI助手、开发工具、数据处理等领域。
"""
    
    # 写入文件
    with open("ai_report.txt", "w", encoding="utf-8") as f:
        f.write(ai_content)
    
    with open("mcp_tech_doc.txt", "w", encoding="utf-8") as f:
        f.write(tech_content)
    
    print("✅ 示例文档创建完成")

def demo_document_processing():
    """演示文档处理功能"""
    print("\n=== 文档处理演示 ===")
    
    # 这里展示如何使用MCP工具（实际使用时需要通过MCP客户端调用）
    print("📄 可用的文档处理工具：")
    print("- parse_document: 解析文档并提取内容")
    print("- search_documents: 搜索文档")
    print("- get_document_content: 获取文档完整内容")
    print("- list_documents: 列出所有文档")
    
    print("\n📋 示例调用：")
    print("1. 解析文档:")
    print('   parse_document("ai_report.txt", extract_keywords=True, generate_summary=True)')
    
    print("\n2. 搜索文档:")
    print('   search_documents("人工智能", search_type="content")')
    
    print("\n3. 获取文档内容:")
    print('   get_document_content(1)')

def demo_knowledge_management():
    """演示知识管理功能"""
    print("\n=== 知识管理演示 ===")
    
    print("🧠 可用的知识管理工具：")
    print("- add_knowledge_entry: 添加知识库条目")
    print("- search_knowledge_base: 搜索知识库")
    print("- get_statistics: 获取系统统计信息")
    
    print("\n📋 示例调用：")
    print("1. 添加知识条目:")
    print('''   add_knowledge_entry(
       title="AI发展趋势",
       content="人工智能技术正在快速发展...",
       category="技术",
       tags=["AI", "技术趋势"]
   )''')
    
    print("\n2. 搜索知识库:")
    print('   search_knowledge_base("人工智能", category="技术")')
    
    print("\n3. 获取统计信息:")
    print('   get_statistics()')

def demo_resources():
    """演示资源访问"""
    print("\n=== 资源访问演示 ===")
    
    print("🔗 可用资源：")
    print("- document://{document_id} - 获取文档资源")
    print("- knowledge://{entry_id} - 获取知识库条目资源")
    
    print("\n📋 示例访问：")
    print("1. 访问文档资源:")
    print('   document://1')
    
    print("\n2. 访问知识库资源:")
    print('   knowledge://1')

def main():
    """主演示函数"""
    print("🚀 智能文档处理与知识管理MCP服务演示")
    print("=" * 50)
    
    # 创建示例文档
    create_sample_documents()
    
    # 演示各功能模块
    demo_document_processing()
    demo_knowledge_management()
    demo_resources()
    
    print("\n" + "=" * 50)
    print("💡 使用说明：")
    print("1. 启动MCP服务器: python document_mcp.py")
    print("2. 通过MCP客户端连接并使用工具")
    print("3. 查看README.md获取详细使用指南")
    
    print("\n🎯 核心价值：")
    print("- 统一的文档处理接口")
    print("- 智能的内容提取和分析")
    print("- 结构化的知识管理")
    print("- 标准化的MCP协议支持")

if __name__ == "__main__":
    main()