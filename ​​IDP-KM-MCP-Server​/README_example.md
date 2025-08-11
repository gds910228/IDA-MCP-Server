# IDP 知识管理 MCP 服务器

一个基于 Model Context Protocol (MCP) 的智能文档解析和知识管理服务器，支持多种文档格式的解析、内容提取、关键词分析和知识库管理。

## 🚀 功能特性

### 📄 文档解析
- **多格式支持**: PDF、Word、Excel、PowerPoint、TXT、Markdown
- **智能提取**: 自动提取文档内容、元数据和结构信息
- **关键词分析**: 基于 TF-IDF 算法的智能关键词提取
- **摘要生成**: 自动生成文档摘要

### 🔍 搜索功能
- **全文搜索**: 支持文档内容的全文检索
- **关键词搜索**: 基于提取的关键词进行精准搜索
- **文件名搜索**: 支持按文件名模糊匹配
- **分类搜索**: 支持按文档分类进行筛选

### 📚 知识库管理
- **知识条目**: 创建和管理结构化知识条目
- **分类标签**: 支持多级分类和标签系统
- **关联文档**: 知识条目与源文档的关联管理
- **版本控制**: 知识条目的版本历史追踪

## 🛠️ 技术架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCP Client    │────│  MCP Server     │────│   SQLite DB     │
│   (Claude/IDE)  │    │  (Python)       │    │  (Documents)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │  Document       │
                       │  Processors     │
                       │  (PDF/Word/etc) │
                       └─────────────────┘
```

### 核心组件
- **MCP 服务器**: 基于 `mcp` 库的标准 MCP 实现
- **文档处理器**: 支持多种格式的文档解析引擎
- **数据库层**: SQLite 数据库存储文档和知识库数据
- **搜索引擎**: 基于 TF-IDF 的全文搜索实现

## 📦 安装部署

### 环境要求
- Python 3.8+
- SQLite 3.x
- 依赖库详见 `requirements.txt`

### 快速开始

1. **克隆项目**
```bash
git clone https://github.com/your-username/idp-km-mcp-server.git
cd idp-km-mcp-server
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动服务器**
```bash
python start_server.py
```

4. **配置 MCP 客户端**
在您的 MCP 客户端配置中添加：
```json
{
  "mcpServers": {
    "mcp-idp-km": {
      "command": "python",
      "args": ["D:/WorkProjects/AI/MCP/IDP-KM-MCP-Server/document_mcp.py"]
    }
  }
}
```

## 🔧 配置说明

### 数据库配置
```python
# config.py
DATABASE_PATH = "documents.db"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
SUPPORTED_FORMATS = ['.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.md']
```

### 文档处理配置
```python
# 关键词提取配置
KEYWORD_COUNT = 10
MIN_KEYWORD_LENGTH = 2
STOP_WORDS = ['的', '是', '在', '了', '和', '与', '或']

# 摘要生成配置
SUMMARY_SENTENCES = 3
SUMMARY_MAX_LENGTH = 500
```

## 📖 API 文档

### MCP 工具 (Tools)

#### `parse_document`
解析文档并提取内容
```python
{
  "filepath": "path/to/document.pdf",
  "extract_keywords": true,
  "generate_summary": true
}
```

#### `search_documents`
搜索文档
```python
{
  "query": "搜索关键词",
  "search_type": "content"  # content, keywords, filename
}
```

#### `add_knowledge_entry`
添加知识库条目
```python
{
  "title": "知识条目标题",
  "content": "详细内容",
  "category": "分类",
  "tags": ["标签1", "标签2"],
  "source_doc_id": 123
}
```

#### `search_knowledge_base`
搜索知识库
```python
{
  "query": "搜索查询",
  "category": "可选分类过滤"
}
```

### MCP 资源 (Resources)

#### `document://{document_id}`
获取指定文档的完整信息

#### `knowledge://{entry_id}`
获取指定知识库条目的详细信息

## 📊 使用示例

### 1. 解析文档
```python
# 通过 MCP 客户端调用
result = mcp_client.call_tool("parse_document", {
    "filepath": "reports/annual_report_2024.pdf",
    "extract_keywords": True,
    "generate_summary": True
})

print(f"文档ID: {result['document_id']}")
print(f"关键词: {result['keywords']}")
print(f"摘要: {result['summary']}")
```

### 2. 搜索文档
```python
# 内容搜索
results = mcp_client.call_tool("search_documents", {
    "query": "财务报告",
    "search_type": "content"
})

for doc in results['documents']:
    print(f"文档: {doc['filename']} (相关度: {doc['relevance']})")
```

### 3. 管理知识库
```python
# 添加知识条目
entry_id = mcp_client.call_tool("add_knowledge_entry", {
    "title": "公司财务分析方法",
    "content": "详细的财务分析步骤和方法...",
    "category": "财务分析",
    "tags": ["财务", "分析", "方法论"],
    "source_doc_id": 123
})

# 搜索知识库
knowledge = mcp_client.call_tool("search_knowledge_base", {
    "query": "财务分析",
    "category": "财务分析"
})
```

## 🔍 高级功能

### 批量文档处理
```python
import os
from pathlib import Path

def batch_process_documents(directory_path):
    """批量处理目录下的所有文档"""
    for file_path in Path(directory_path).rglob("*"):
        if file_path.suffix.lower() in SUPPORTED_FORMATS:
            result = parse_document(str(file_path))
            print(f"已处理: {file_path.name}")
```

### 自定义关键词提取
```python
def custom_keyword_extraction(text, custom_stop_words=None):
    """自定义关键词提取逻辑"""
    # 实现自定义的关键词提取算法
    pass
```

### 知识图谱构建
```python
def build_knowledge_graph():
    """基于文档和知识库构建知识图谱"""
    # 分析文档间的关联关系
    # 构建知识节点和边
    pass
```

## 📈 性能优化

### 数据库优化
- 为搜索字段创建索引
- 定期清理过期数据
- 使用连接池管理数据库连接

### 文档处理优化
- 异步处理大文件
- 缓存处理结果
- 分块处理超大文档

### 搜索优化
- 实现搜索结果缓存
- 优化 TF-IDF 计算
- 支持模糊匹配和同义词

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_document_parser.py

# 生成覆盖率报告
python -m pytest --cov=src tests/
```

### 测试用例
- 文档解析测试
- 搜索功能测试
- 知识库管理测试
- MCP 协议兼容性测试

## 🚀 部署指南

### Docker 部署
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "start_server.py"]
```

### 生产环境配置
```bash
# 使用 gunicorn 部署
gunicorn --bind 0.0.0.0:8000 --workers 4 start_server:app

# 使用 systemd 管理服务
sudo systemctl enable idp-km-mcp
sudo systemctl start idp-km-mcp
```

## 🤝 贡献指南

### 开发环境设置
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -r requirements-dev.txt

# 安装 pre-commit 钩子
pre-commit install
```

### 代码规范
- 遵循 PEP 8 代码风格
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 编写完整的文档字符串

### 提交流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📋 路线图

### v1.0 (当前版本)
- [x] 基础文档解析功能
- [x] 简单搜索功能
- [x] 知识库管理
- [x] MCP 协议支持

### v1.1 (计划中)
- [ ] 增强的搜索算法
- [ ] 文档版本控制
- [ ] 批量操作 API
- [ ] 性能监控

### v2.0 (未来版本)
- [ ] 知识图谱可视化
- [ ] AI 驱动的内容分析
- [ ] 多语言支持
- [ ] 分布式部署支持

## 🐛 问题反馈

如果您遇到任何问题或有功能建议，请通过以下方式联系我们：

- **GitHub Issues**: [创建 Issue](https://github.com/your-username/idp-km-mcp-server/issues)
- **邮箱**: your-email@example.com
- **讨论区**: [GitHub Discussions](https://github.com/your-username/idp-km-mcp-server/discussions)

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

感谢以下开源项目和贡献者：

- [Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk) - MCP 协议实现
- [PyPDF2](https://github.com/py-pdf/PyPDF2) - PDF 文档处理
- [python-docx](https://github.com/python-openxml/python-docx) - Word 文档处理
- [scikit-learn](https://github.com/scikit-learn/scikit-learn) - 机器学习算法

---

<div align="center">
  <p>如果这个项目对您有帮助，请给我们一个 ⭐️</p>
  <p>Made with ❤️ by IDP Team</p>
</div>