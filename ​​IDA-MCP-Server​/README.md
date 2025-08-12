# 智能开发助手MCP服务

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 为AI助手提供强大的开发工具集成能力的MCP服务

## 🎯 项目简介

智能开发助手MCP服务是一个基于Model Context Protocol (MCP)的通用型服务，专为蓝耘科技MCP挑战赛开发。它为AI助手提供了丰富的代码分析、项目管理和开发辅助功能。

### 核心特性

- 🔍 **智能代码分析**: 支持Python、JavaScript/TypeScript的质量分析
- 📊 **复杂度计算**: 圈复杂度分析和代码健康度评估  
- 🏗️ **项目结构分析**: 全面的项目组织和文件统计
- 📝 **智能提示生成**: 代码审查和重构建议
- 🔧 **动态资源访问**: 实时获取项目信息和指标

## 🚀 快速开始

### 环境要求

- Python 3.8+
- FastMCP框架
- 支持MCP协议的AI助手

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd mcp3
```

2. **安装依赖**
```bash
pip install -r requirements.txt
# 或使用uv
uv sync
```

3. **运行服务**
```bash
python main.py
```

4. **测试功能**
```bash
python test_mcp_service.py
```

## 📋 功能详解

### 🔧 MCP工具 (Tools)

#### 代码分析工具
- `analyze_code(file_path)`: 分析代码质量、复杂度和潜在问题
- `calculate_complexity(file_path)`: 计算代码圈复杂度
- `analyze_project_structure(project_path)`: 分析项目整体结构

#### 使用示例
```python
# 通过AI助手调用
analyze_code("src/main.py")
# 返回: 质量评分、问题列表、复杂度等详细信息

analyze_project_structure("./my-project")
# 返回: 文件统计、语言分布、目录结构等
```

### 📊 动态资源 (Resources)

#### 项目信息资源
- `project://info/{path}`: 获取项目或文件的基本信息
- `project://metrics/{path}`: 获取详细的项目指标数据

#### 使用示例
```
# 访问项目信息
project://info/src/main.py

# 获取项目指标
project://metrics/./
```

### 💡 智能提示 (Prompts)

#### 代码审查提示
- `code_review_prompt(file_path, focus_area)`: 生成专业的代码审查提示
- `refactor_suggestions_prompt(file_path, complexity_threshold)`: 生成重构建议

#### 使用示例
```python
# 生成代码审查提示
code_review_prompt("src/complex_module.py", "security")

# 生成重构建议
refactor_suggestions_prompt("src/legacy_code.py", 10)
```

## 📈 测试结果示例

### 代码质量分析
```json
{
  "file_path": "test_example.py",
  "language": "python",
  "lines_of_code": 129,
  "functions": 5,
  "classes": 1,
  "complexity_score": 25,
  "quality_score": 90,
  "issues": [
    {
      "type": "complexity",
      "severity": "warning",
      "line": 10,
      "message": "Function 'complex_function' is too complex (complexity: 18)"
    }
  ]
}
```

### 项目结构分析
```json
{
  "project_path": ".",
  "total_files": 11,
  "code_files": 6,
  "languages": {
    "Python": 6
  },
  "directories": ["docs", "src", "src/tools"],
  "files_by_type": {
    ".py": 6,
    ".md": 3,
    ".toml": 1
  }
}
```

## 🏆 竞赛优势

### 通用型服务特点
- ✅ **广泛适用性**: 支持多种编程语言和项目类型
- ✅ **功能完善**: 涵盖分析、评估、建议的完整工作流
- ✅ **易于集成**: 标准MCP协议，兼容各种AI助手
- ✅ **实用价值**: 直接解决开发者日常痛点

### 技术亮点
- 🔥 基于AST的深度代码分析
- 🔥 智能复杂度计算算法
- 🔥 多语言支持架构
- 🔥 动态资源和智能提示系统

## 📁 项目结构

```
mcp3/
├── src/                    # 源代码目录
│   ├── tools/             # 工具模块
│   │   ├── code_analyzer.py  # 代码分析器
│   │   └── __init__.py
│   └── __init__.py
├── docs/                  # 文档目录
│   ├── PRD.md            # 产品需求文档
│   └── tasks.md          # 任务管理
├── main.py               # MCP服务主文件
├── test_example.py       # 测试示例文件
├── test_mcp_service.py   # 服务测试脚本
├── pyproject.toml        # 项目配置
└── README.md            # 项目说明
```

## 🔮 未来规划

### Phase 2 功能扩展
- [ ] 支持更多编程语言 (Java, C++, Go)
- [ ] 集成更多静态分析工具
- [ ] 添加安全漏洞扫描功能
- [ ] 实现自动化文档生成

### Phase 3 高级特性
- [ ] 可视化分析报告
- [ ] 团队协作功能
- [ ] CI/CD集成
- [ ] 云服务部署

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🏅 竞赛信息

本项目参与蓝耘科技MCP挑战赛，专注于**通用型服务**赛道，致力于为AI助手提供强大的开发工具集成能力。

---

**让AI助手成为更智能的开发伙伴！** 🚀