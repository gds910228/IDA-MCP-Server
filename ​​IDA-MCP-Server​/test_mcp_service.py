"""
MCP服务测试脚本
"""

import sys
import os
sys.path.append('.')

from src.tools.code_analyzer import CodeAnalyzer
import json


def test_code_analyzer():
    """测试代码分析器"""
    print("🔍 测试代码分析功能...")
    
    analyzer = CodeAnalyzer()
    
    # 测试Python文件分析
    print("\n📊 分析Python测试文件:")
    result = analyzer.analyze_code_quality("test_example.py")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 测试项目结构分析
    print("\n📁 分析项目结构:")
    structure = analyzer.analyze_project_structure(".")
    print(json.dumps(structure, indent=2, ensure_ascii=False))


def test_main_py_analysis():
    """测试主文件分析"""
    print("\n🔍 分析main.py文件:")
    
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_code_quality("main.py")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    print("🚀 开始测试智能开发助手MCP服务")
    print("=" * 50)
    
    test_code_analyzer()
    test_main_py_analysis()
    
    print("\n✅ 测试完成!")
    print("\n💡 使用方法:")
    print("1. 运行MCP服务: python main.py")
    print("2. 连接AI助手，使用以下工具:")
    print("   - analyze_code(file_path): 分析代码质量")
    print("   - analyze_project_structure(project_path): 分析项目结构")
    print("   - calculate_complexity(file_path): 计算复杂度")