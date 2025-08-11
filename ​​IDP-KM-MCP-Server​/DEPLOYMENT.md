# 智能文档处理与知识管理MCP - 部署指南

## 快速开始

### 1. 环境准备
```bash
# 确保Python版本
python --version  # 需要 Python 3.8+

# 克隆或下载项目文件
# 确保以下文件存在：
# - document_mcp.py
# - requirements.txt
# - config.py
# - start_server.py
```

### 2. 安装依赖
```bash
# 安装核心依赖
pip install mcp fastmcp

# 安装可选依赖（推荐）
pip install PyPDF2 python-docx jieba

# 或一次性安装所有依赖
pip install -r requirements.txt
```

### 3. 启动服务
```bash
# 方式1: 使用启动脚本（推荐）
python start_server.py

# 方式2: 直接启动
python document_mcp.py

# 方式3: 指定传输方式
python -c "from document_mcp import mcp; mcp.run(transport='stdio')"
```

## 详细部署

### 系统要求
- **操作系统**: Windows, macOS, Linux
- **Python版本**: 3.8 或更高
- **内存**: 最少 256MB，推荐 512MB+
- **存储**: 根据文档数量，建议预留 1GB+

### 依赖说明

#### 必需依赖
```bash
pip install mcp fastmcp
```

#### 可选依赖
```bash
# PDF文档处理
pip install PyPDF2

# Word文档处理  
pip install python-docx

# 中文文本处理
pip install jieba
```

### 配置选项

编辑 `config.py` 文件自定义配置：

```python
# 数据库路径
DATABASE_CONFIG["path"] = "custom_path/documents.db"

# 最大文件大小 (字节)
DOCUMENT_CONFIG["max_file_size"] = 100 * 1024 * 1024  # 100MB

# 支持的文件扩展名
DOCUMENT_CONFIG["supported_extensions"] = [".txt", ".pdf", ".docx"]

# 功能开关
FEATURES["pdf_processing"] = True
FEATURES["chinese_processing"] = True
```

### 数据库初始化

服务器首次启动时会自动创建数据库：
```
documents.db
├── documents 表 (文档信息)
└── knowledge_base 表 (知识库条目)
```

### 测试部署

```bash
# 运行测试脚本
python test_mcp.py

# 运行使用示例
python example_usage.py
```

## MCP客户端连接

### 连接配置
```json
{
  "mcpServers": {
    "document-processor": {
      "command": "python",
      "args": ["path/to/document_mcp.py"],
      "transport": "stdio"
    }
  }
}
```

### 可用工具
- `parse_document` - 解析文档
- `search_documents` - 搜索文档
- `get_document_content` - 获取文档内容
- `add_knowledge_entry` - 添加知识条目
- `search_knowledge_base` - 搜索知识库
- `list_documents` - 列出文档
- `get_statistics` - 获取统计信息

### 可用资源
- `document://{id}` - 文档资源
- `knowledge://{id}` - 知识库资源

## 生产环境部署

### Docker部署 (推荐)

创建 `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "document_mcp.py"]
```

构建和运行：
```bash
docker build -t document-mcp .
docker run -p 8000:8000 -v $(pwd)/data:/app/data document-mcp
```

### 系统服务部署

创建 systemd 服务文件 `/etc/systemd/system/document-mcp.service`:
```ini
[Unit]
Description=Document Processing MCP Server
After=network.target

[Service]
Type=simple
User=mcp
WorkingDirectory=/opt/document-mcp
ExecStart=/usr/bin/python3 document_mcp.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl enable document-mcp
sudo systemctl start document-mcp
sudo systemctl status document-mcp
```

### 性能优化

1. **数据库优化**
   ```python
   # 在config.py中调整
   DATABASE_CONFIG["timeout"] = 60.0
   ```

2. **内存优化**
   ```python
   # 限制最大文件大小
   DOCUMENT_CONFIG["max_file_size"] = 10 * 1024 * 1024  # 10MB
   ```

3. **并发处理**
   - 使用进程池处理大文件
   - 实现异步文档处理

### 监控和日志

1. **日志配置**
   ```python
   LOGGING_CONFIG = {
       "level": "INFO",
       "file": "/var/log/document-mcp.log"
   }
   ```

2. **健康检查**
   ```bash
   # 检查服务状态
   curl -f http://localhost:8000/health || exit 1
   ```

### 安全考虑

1. **文件访问限制**
   - 限制可访问的文件路径
   - 验证文件类型和大小

2. **数据库安全**
   - 定期备份数据库
   - 设置适当的文件权限

3. **网络安全**
   - 使用HTTPS传输
   - 实现访问控制

## 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   
   # 使用国内镜像
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
   ```

2. **PDF处理失败**
   ```bash
   # 安装额外依赖
   pip install PyPDF2 pdfplumber
   ```

3. **中文处理问题**
   ```bash
   # 安装中文处理库
   pip install jieba
   ```

4. **数据库锁定**
   ```bash
   # 检查数据库文件权限
   chmod 664 documents.db
   ```

### 日志分析
```bash
# 查看服务日志
tail -f mcp_server.log

# 查看系统日志
journalctl -u document-mcp -f
```

### 性能监控
```bash
# 监控资源使用
htop
iostat -x 1

# 监控数据库大小
du -h documents.db
```

## 升级指南

### 版本升级
1. 备份数据库文件
2. 更新代码文件
3. 安装新依赖
4. 重启服务

### 数据迁移
```python
# 数据库结构变更时的迁移脚本
import sqlite3

def migrate_database():
    conn = sqlite3.connect('documents.db')
    # 执行迁移SQL
    conn.execute('ALTER TABLE documents ADD COLUMN new_field TEXT')
    conn.commit()
    conn.close()
```

## 支持与维护

- **文档**: 查看 README.md
- **示例**: 运行 example_usage.py
- **测试**: 运行 test_mcp.py
- **配置**: 编辑 config.py

---

🎉 **部署完成！** 您的智能文档处理与知识管理MCP服务现在已经可以使用了。