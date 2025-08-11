"""
MCP服务器启动脚本
"""

import sys
import subprocess
import os

def check_dependencies():
    """检查依赖是否安装"""
    print("🔍 检查依赖...")
    
    required_packages = [
        'mcp',
        'fastmcp'
    ]
    
    optional_packages = [
        ('PyPDF2', 'PDF文档处理'),
        ('docx', 'Word文档处理'),
        ('jieba', '中文分词')
    ]
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_required.append(package)
            print(f"❌ {package} (必需)")
    
    for package, description in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package} - {description}")
        except ImportError:
            missing_optional.append((package, description))
            print(f"⚠️ {package} - {description} (可选)")
    
    if missing_required:
        print(f"\n❌ 缺少必需依赖: {', '.join(missing_required)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    if missing_optional:
        print(f"\n⚠️ 缺少可选依赖，某些功能可能不可用")
        print("建议安装: pip install PyPDF2 python-docx jieba")
    
    return True

def start_server():
    """启动MCP服务器"""
    print("\n🚀 启动智能文档处理与知识管理MCP服务器...")
    
    try:
        # 导入并启动服务器
        from document_mcp import mcp
        
        print("✅ 服务器模块加载成功")
        print("🌐 服务器启动中...")
        print("\n" + "="*50)
        print("📚 智能文档处理与知识管理MCP服务")
        print("="*50)
        print("🔧 支持功能:")
        print("  - 文档解析 (TXT, PDF, DOCX)")
        print("  - 关键词提取")
        print("  - 摘要生成")
        print("  - 知识库管理")
        print("  - 智能搜索")
        print("\n💡 使用方法:")
        print("  通过MCP客户端连接此服务器")
        print("  使用提供的工具进行文档处理")
        print("\n🛑 按 Ctrl+C 停止服务器")
        print("="*50)
        
        # 启动服务器
        mcp.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 服务器启动失败: {e}")
        print("请检查配置和依赖")

def main():
    """主函数"""
    print("🎯 智能文档处理与知识管理MCP服务器")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main()