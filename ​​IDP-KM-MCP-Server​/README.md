# 智能文档处理与知识管理MCP服务器

一个基于 Model Context Protocol (MCP) 的智能文档处理与知识管理服务器，支持多种文档格式的解析、内容提取、关键词提取、摘要生成和知识库管理。

## 🚀 功能特性

- 📄 **多格式文档解析**：支持 TXT、PDF、DOCX 文档格式
- 🔍 **智能关键词提取**：基于 jieba 分词的中文关键词提取
- 📝 **自动摘要生成**：智能生成文档摘要
- 📚 **知识库管理**：结构化存储和管理知识条目
- 🔎 **智能搜索**：支持内容、关键词、文件名多维度搜索
- 💾 **SQLite 数据库**：轻量级本地数据存储

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

### 依赖包说明

- `mcp>=1.12.3` - Model Context Protocol 核心库
- `fastmcp` - 快速 MCP 服务器框架
- `PyPDF2>=3.0.0` - PDF 文档处理
- `python-docx>=0.8.11` - Word 文档处理
- `jieba>=0.42.1` - 中文分词和关键词提取

## 🛠️ 使用方法

### 启动服务器

```bash
python document_mcp.py
```

或使用启动脚本：

```bash
python start_server.py
```

### MCP 配置

在你的 MCP 客户端配置文件中添加：

```json
{
  "mcpServers": {
    "mcp-idp-km": {
      "disabled": false,
      "timeout": 60,
      "type": "stdio",
      "command": "python",
      "args": [
        "path/to/document_mcp.py"
      ]
    }
  }
}
```

## 🔧 可用工具

### 文档处理工具

- `parse_document` - 解析文档并提取内容
- `search_documents` - 搜索文档
- `get_document_content` - 获取文档完整内容
- `list_documents` - 列出所有文档

### 知识库管理工具

- `add_knowledge_entry` - 添加知识库条目
- `search_knowledge_base` - 搜索知识库
- `get_statistics` - 获取系统统计信息

## 📊 数据库结构

### documents 表
- `id` - 文档ID
- `filename` - 文件名
- `filepath` - 文件路径
- `file_hash` - 文件哈希值
- `content` - 文档内容
- `summary` - 文档摘要
- `keywords` - 关键词（JSON格式）
- `tags` - 标签（JSON格式）
- `created_at` - 创建时间
- `updated_at` - 更新时间

### knowledge_base 表
- `id` - 条目ID
- `title` - 标题
- `content` - 内容
- `category` - 分类
- `tags` - 标签（JSON格式）
- `source_doc_id` - 来源文档ID
- `created_at` - 创建时间

## 🌟 使用示例

### 解析文档
```python
# 通过 MCP 客户端调用
result = parse_document(
    filepath="example.pdf",
    extract_keywords=True,
    generate_summary=True
)
```

### 搜索文档
```python
# 搜索包含特定内容的文档
documents = search_documents(
    query="人工智能",
    search_type="content"
)
```

### 添加知识条目
```python
# 添加新的知识库条目
entry = add_knowledge_entry(
    title="机器学习基础",
    content="机器学习是人工智能的一个分支...",
    category="技术",
    tags=["AI", "机器学习", "算法"]
)
```

## 🔍 资源访问

服务器提供以下资源模板：

- `document://{document_id}` - 访问特定文档
- `knowledge://{entry_id}` - 访问特定知识库条目

## 📝 开发说明

### 项目结构
```
├── document_mcp.py      # 主服务器文件
├── start_server.py      # 启动脚本
├── requirements.txt     # 依赖配置
├── pyproject.toml      # 项目配置
├── documents.db        # SQLite 数据库（运行时生成）
└── README.md           # 项目说明
```

### 扩展功能

你可以通过以下方式扩展功能：

1. 添加新的文档格式支持
2. 集成更高级的NLP处理
3. 添加向量化搜索
4. 集成外部知识库

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)