"""
智能开发助手MCP服务

为AI助手提供强大的开发工具集成能力，包括代码分析、文档生成、依赖管理等功能。
"""

import json
import os
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
from src.tools.code_analyzer import CodeAnalyzer

# Create MCP server
mcp = FastMCP("智能开发助手")

# Initialize code analyzer
analyzer = CodeAnalyzer()


# 代码分析工具
@mcp.tool()
def analyze_code(file_path: str) -> str:
    """
    分析代码文件的质量、复杂度和潜在问题
    
    Args:
        file_path: 要分析的代码文件路径
    
    Returns:
        JSON格式的分析结果，包含质量评分、问题列表、复杂度等信息
    """
    result = analyzer.analyze_code_quality(file_path)
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
def analyze_project_structure(project_path: str) -> str:
    """
    分析项目结构，统计文件类型、编程语言分布等信息
    
    Args:
        project_path: 项目根目录路径
    
    Returns:
        JSON格式的项目结构分析结果
    """
    result = analyzer.analyze_project_structure(project_path)
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
def calculate_complexity(file_path: str) -> str:
    """
    计算代码文件的圈复杂度
    
    Args:
        file_path: 要分析的代码文件路径
    
    Returns:
        JSON格式的复杂度分析结果
    """
    analysis = analyzer.analyze_code_quality(file_path)
    if "error" in analysis:
        return json.dumps(analysis, ensure_ascii=False)
    
    complexity_result = {
        "file_path": file_path,
        "complexity_score": analysis.get("complexity_score", 0),
        "functions_count": analysis.get("functions", 0),
        "classes_count": analysis.get("classes", 0),
        "complexity_level": "low" if analysis.get("complexity_score", 0) < 10 else 
                           "medium" if analysis.get("complexity_score", 0) < 20 else "high"
    }
    
    return json.dumps(complexity_result, indent=2, ensure_ascii=False)


# 动态资源：项目信息
@mcp.resource("project://info/{path}")
def get_project_info(path: str) -> str:
    """获取项目基本信息"""
    if not os.path.exists(path):
        return json.dumps({"error": f"Path not found: {path}"}, ensure_ascii=False)
    
    info = {
        "path": path,
        "is_directory": os.path.isdir(path),
        "exists": True
    }
    
    if os.path.isdir(path):
        # 项目目录信息
        structure = analyzer.analyze_project_structure(path)
        info.update(structure)
    else:
        # 单个文件信息
        analysis = analyzer.analyze_code_quality(path)
        info.update(analysis)
    
    return json.dumps(info, indent=2, ensure_ascii=False)


@mcp.resource("project://metrics/{path}")
def get_project_metrics(path: str) -> str:
    """获取项目指标数据"""
    if not os.path.exists(path):
        return json.dumps({"error": f"Path not found: {path}"}, ensure_ascii=False)
    
    if os.path.isfile(path):
        # 单文件指标
        analysis = analyzer.analyze_code_quality(path)
        metrics = {
            "file_metrics": {
                "lines_of_code": analysis.get("lines_of_code", 0),
                "quality_score": analysis.get("quality_score", 0),
                "complexity_score": analysis.get("complexity_score", 0),
                "issues_count": len(analysis.get("issues", []))
            }
        }
    else:
        # 项目整体指标
        structure = analyzer.analyze_project_structure(path)
        metrics = {
            "project_metrics": {
                "total_files": structure.get("total_files", 0),
                "code_files": structure.get("code_files", 0),
                "languages": structure.get("languages", {}),
                "directories_count": len(structure.get("directories", []))
            }
        }
    
    return json.dumps(metrics, indent=2, ensure_ascii=False)


# 智能提示：代码审查
@mcp.prompt()
def code_review_prompt(file_path: str, focus_area: str = "general") -> str:
    """
    生成代码审查提示
    
    Args:
        file_path: 要审查的文件路径
        focus_area: 关注领域 (general, security, performance, maintainability)
    """
    focus_areas = {
        "general": "进行全面的代码审查，关注代码质量、可读性和最佳实践",
        "security": "重点关注安全漏洞、输入验证和潜在的安全风险",
        "performance": "专注于性能优化、算法效率和资源使用",
        "maintainability": "评估代码的可维护性、模块化程度和文档完整性"
    }
    
    focus_desc = focus_areas.get(focus_area, focus_areas["general"])
    
    return f"""请对文件 {file_path} 进行代码审查。

审查重点：{focus_desc}

请按以下结构提供审查意见：

## 代码质量评估
- 整体代码质量评分
- 主要优点
- 需要改进的地方

## 具体问题与建议
- 列出发现的具体问题
- 提供改进建议和最佳实践

## 重构建议
- 如有需要，提供重构方案
- 优先级排序

请基于实际的代码分析结果提供专业、具体的审查意见。"""


@mcp.prompt()
def refactor_suggestions_prompt(file_path: str, complexity_threshold: int = 10) -> str:
    """
    生成重构建议提示
    
    Args:
        file_path: 要重构的文件路径
        complexity_threshold: 复杂度阈值
    """
    return f"""请为文件 {file_path} 提供重构建议。

重构目标：
- 降低代码复杂度（目标：复杂度 < {complexity_threshold}）
- 提高代码可读性和可维护性
- 遵循SOLID原则和设计模式

请提供：

## 重构优先级
1. 高优先级：影响功能正确性和安全性的问题
2. 中优先级：影响性能和可维护性的问题  
3. 低优先级：代码风格和最佳实践改进

## 具体重构方案
- 函数拆分建议
- 类设计优化
- 代码结构调整
- 设计模式应用

## 重构步骤
- 详细的重构执行步骤
- 每步的风险评估
- 测试验证方案

请基于代码分析结果提供切实可行的重构方案。"""

if __name__ == "__main__":
    # Start the server
    mcp.run(transport="stdio")