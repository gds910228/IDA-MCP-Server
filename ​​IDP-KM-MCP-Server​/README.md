# 智能文档处理与知识管理MCP服务器

这是一个基于MCP协议的智能文档处理与知识管理服务，提供文档解析、内容提取、知识管理等功能。

## 功能特性

### 🔍 文档处理
- **多格式支持**: TXT, PDF, DOCX文档解析
- **智能提取**: 自动提取文档内容、关键词、摘要
- **去重处理**: 基于文件哈希的重复文档检测

### 📚 知识管理
- **知识库**: 结构化存储知识条目
- **分类管理**: 支持分类和标签系统
- **智能搜索**: 多维度搜索功能

### 🔧 核心工具

#### 文档处理工具
- `parse_document`: 解析文档并提取内容
- `get_document_content`: 获取文档完整内容
- `list_documents`: 列出所有文档
- `search_documents`: 搜索文档

#### 知识管理工具
- `add_knowledge_entry`: 添加知识库条目
- `search_knowledge_base`: 搜索知识库
- `get_statistics`: 获取系统统计信息

## 安装与使用

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务器
```bash
python document_mcp.py
```

### 3. 使用示例

#### 解析文档
```python
# 解析PDF文档
result = parse_document("example.pdf", extract_keywords=True, generate_summary=True)
```

#### 搜索文档
```python
# 按内容搜索
documents = search_documents("人工智能", search_type="content")

# 按文件名搜索
documents = search_documents("报告", search_type="filename")
```

#### 添加知识条目
```python
# 添加知识库条目
result = add_knowledge_entry(
    title="AI发展趋势",
    content="人工智能技术正在快速发展...",
    category="技术",
    tags=["AI", "技术趋势"]
)
```

## 数据存储

系统使用SQLite数据库存储文档和知识库数据：
- `documents.db`: 主数据库文件
- `documents`: 文档信息表
- `knowledge_base`: 知识库条目表

## 支持的文件格式

- **TXT**: 纯文本文件（UTF-8/GBK编码）
- **PDF**: PDF文档（需要PyPDF2）
- **DOCX**: Word文档（需要python-docx）

## API接口

### 工具接口
所有工具都通过MCP协议暴露，支持：
- 参数验证
- 错误处理
- 结果格式化

### 资源接口
- `document://{document_id}`: 获取文档资源
- `knowledge://{entry_id}`: 获取知识库条目资源

## 扩展功能

### 可选依赖
- `jieba`: 中文分词和关键词提取
- `PyPDF2`: PDF文档处理
- `python-docx`: Word文档处理

### 自定义扩展
系统设计支持：
- 新文档格式处理器
- 自定义关键词提取算法
- 高级摘要生成
- 多语言支持

## 性能特性

- **增量处理**: 基于文件哈希的重复检测
- **轻量级**: SQLite数据库，无需额外服务
- **可扩展**: 模块化设计，易于扩展

## 使用场景

1. **企业文档管理**: 处理和管理企业内部文档
2. **学术研究**: 论文和资料的整理分析
3. **知识库构建**: 构建结构化知识库
4. **内容分析**: 文档内容的智能分析和提取

## 技术架构

- **MCP协议**: 标准化的AI工具接口
- **FastMCP**: 快速MCP服务器框架
- **SQLite**: 轻量级数据库存储
- **Python生态**: 丰富的文档处理库

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License