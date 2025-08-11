#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能文档处理与知识管理MCP服务器
支持文档解析、内容提取、知识管理等功能
"""

import os
import json
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import re
import sys

# 确保正确的导入路径
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("错误：无法导入 FastMCP，请确保已安装 fastmcp")
    sys.exit(1)

try:
    from mcp.types import TextContent, ImageContent, EmbeddedResource
except ImportError:
    # 如果无法导入这些类型，使用基本类型
    TextContent = str
    ImageContent = str
    EmbeddedResource = str

# 尝试导入可选依赖
pdf_available = False
docx_available = False
jieba_available = False

try:
    import PyPDF2
    pdf_available = True
except ImportError:
    PyPDF2 = None

try:
    from docx import Document
    docx_available = True
except ImportError:
    Document = None

try:
    import jieba
    import jieba.analyse
    jieba_available = True
except ImportError:
    jieba = None

# 创建MCP服务器
mcp = FastMCP("DocumentProcessor")

# 数据库初始化
DB_PATH = "documents.db"

def init_database():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建文档表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            file_hash TEXT UNIQUE NOT NULL,
            content TEXT,
            summary TEXT,
            keywords TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建知识库表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            tags TEXT,
            source_doc_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_doc_id) REFERENCES documents (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# 初始化数据库
init_database()

class DocumentProcessor:
    """文档处理器"""
    
    @staticmethod
    def calculate_file_hash(filepath: str) -> str:
        """计算文件哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            return f"error_{str(e)}"
    
    @staticmethod
    def extract_text_from_txt(filepath: str) -> str:
        """从TXT文件提取文本"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='gbk') as f:
                return f.read()
        except Exception as e:
            return f"Error reading TXT file: {str(e)}"
    
    @staticmethod
    def extract_text_from_pdf(filepath: str) -> str:
        """从PDF文件提取文本"""
        if not pdf_available or PyPDF2 is None:
            return "PDF processing not available. Please install PyPDF2: pip install PyPDF2"
        
        try:
            text = ""
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"
    
    @staticmethod
    def extract_text_from_docx(filepath: str) -> str:
        """从DOCX文件提取文本"""
        if not docx_available or Document is None:
            return "DOCX processing not available. Please install python-docx: pip install python-docx"
        
        try:
            doc = Document(filepath)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX file: {str(e)}"
    
    @staticmethod
    def extract_keywords(text: str, topK: int = 10) -> List[str]:
        """提取关键词"""
        if not jieba_available or jieba is None:
            # 简单的关键词提取（基于词频）
            words = re.findall(r'\b\w+\b', text.lower())
            word_freq = {}
            for word in words:
                if len(word) > 2:  # 过滤短词
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # 排序并返回前topK个
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word for word, freq in sorted_words[:topK]]
        
        try:
            # 使用jieba提取关键词
            keywords = jieba.analyse.extract_tags(text, topK=topK, withWeight=False)
            return keywords
        except Exception as e:
            return [f"Error extracting keywords: {str(e)}"]
    
    @staticmethod
    def generate_summary(text: str, max_sentences: int = 3) -> str:
        """生成文档摘要（简单实现）"""
        sentences = re.split(r'[.!?。！？]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if len(sentences) <= max_sentences:
            return '. '.join(sentences)
        
        # 简单选择前几句作为摘要
        summary_sentences = sentences[:max_sentences]
        return '. '.join(summary_sentences) + '.'

# MCP工具定义

@mcp.tool()
def parse_document(filepath: str, extract_keywords: bool = True, generate_summary: bool = True) -> Dict[str, Any]:
    """
    解析文档并提取内容
    
    Args:
        filepath: 文档文件路径
        extract_keywords: 是否提取关键词
        generate_summary: 是否生成摘要
    """
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}"}
    
    # 获取文件信息
    filename = os.path.basename(filepath)
    file_extension = Path(filepath).suffix.lower()
    file_hash = DocumentProcessor.calculate_file_hash(filepath)
    
    # 检查是否已处理过
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE file_hash = ?", (file_hash,))
    existing_doc = cursor.fetchone()
    
    if existing_doc:
        conn.close()
        return {
            "message": "Document already processed",
            "document_id": existing_doc[0],
            "filename": existing_doc[1],
            "content_preview": existing_doc[4][:200] + "..." if existing_doc[4] else ""
        }
    
    # 根据文件类型提取文本
    if file_extension == '.txt':
        content = DocumentProcessor.extract_text_from_txt(filepath)
    elif file_extension == '.pdf':
        content = DocumentProcessor.extract_text_from_pdf(filepath)
    elif file_extension in ['.docx', '.doc']:
        content = DocumentProcessor.extract_text_from_docx(filepath)
    else:
        conn.close()
        return {"error": f"Unsupported file type: {file_extension}"}
    
    # 提取关键词
    keywords = []
    if extract_keywords and content:
        keywords = DocumentProcessor.extract_keywords(content)
    
    # 生成摘要
    summary = ""
    if generate_summary and content:
        summary = DocumentProcessor.generate_summary(content)
    
    # 保存到数据库
    try:
        cursor.execute('''
            INSERT INTO documents (filename, filepath, file_hash, content, summary, keywords, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (filename, filepath, file_hash, content, summary, json.dumps(keywords), datetime.now()))
        
        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "document_id": doc_id,
            "filename": filename,
            "content_length": len(content),
            "keywords": keywords,
            "summary": summary,
            "content_preview": content[:200] + "..." if len(content) > 200 else content
        }
        
    except Exception as e:
        conn.close()
        return {"error": f"Database error: {str(e)}"}

@mcp.tool()
def search_documents(query: str, search_type: str = "content") -> List[Dict[str, Any]]:
    """
    搜索文档
    
    Args:
        query: 搜索查询
        search_type: 搜索类型 (content, keywords, filename)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if search_type == "content":
        cursor.execute('''
            SELECT id, filename, summary, keywords, created_at 
            FROM documents 
            WHERE content LIKE ? OR summary LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
    elif search_type == "keywords":
        cursor.execute('''
            SELECT id, filename, summary, keywords, created_at 
            FROM documents 
            WHERE keywords LIKE ?
        ''', (f'%{query}%',))
    elif search_type == "filename":
        cursor.execute('''
            SELECT id, filename, summary, keywords, created_at 
            FROM documents 
            WHERE filename LIKE ?
        ''', (f'%{query}%',))
    else:
        conn.close()
        return [{"error": "Invalid search_type. Use: content, keywords, or filename"}]
    
    results = cursor.fetchall()
    conn.close()
    
    documents = []
    for row in results:
        doc_id, filename, summary, keywords_json, created_at = row
        try:
            keywords = json.loads(keywords_json) if keywords_json else []
        except:
            keywords = []
        
        documents.append({
            "id": doc_id,
            "filename": filename,
            "summary": summary,
            "keywords": keywords,
            "created_at": created_at
        })
    
    return documents

@mcp.tool()
def get_document_content(document_id: int) -> Dict[str, Any]:
    """
    获取文档完整内容
    
    Args:
        document_id: 文档ID
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE id = ?", (document_id,))
    doc = cursor.fetchone()
    conn.close()
    
    if not doc:
        return {"error": f"Document with ID {document_id} not found"}
    
    return {
        "id": doc[0],
        "filename": doc[1],
        "filepath": doc[2],
        "content": doc[4],
        "summary": doc[5],
        "keywords": json.loads(doc[6]) if doc[6] else [],
        "tags": json.loads(doc[7]) if doc[7] else [],
        "created_at": doc[8],
        "updated_at": doc[9]
    }

@mcp.tool()
def add_knowledge_entry(title: str, content: str, category: str = "", tags: Optional[List[str]] = None, source_doc_id: Optional[int] = None) -> Dict[str, Any]:
    """
    添加知识库条目
    
    Args:
        title: 知识条目标题
        content: 知识内容
        category: 分类
        tags: 标签列表
        source_doc_id: 来源文档ID
    """
    if tags is None:
        tags = []
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO knowledge_base (title, content, category, tags, source_doc_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, content, category, json.dumps(tags), source_doc_id, datetime.now()))
        
        entry_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "entry_id": entry_id,
            "title": title,
            "category": category,
            "tags": tags
        }
        
    except Exception as e:
        conn.close()
        return {"error": f"Database error: {str(e)}"}

@mcp.tool()
def search_knowledge_base(query: str, category: str = "") -> List[Dict[str, Any]]:
    """
    搜索知识库
    
    Args:
        query: 搜索查询
        category: 分类过滤
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if category:
        cursor.execute('''
            SELECT id, title, content, category, tags, created_at 
            FROM knowledge_base 
            WHERE (title LIKE ? OR content LIKE ?) AND category = ?
        ''', (f'%{query}%', f'%{query}%', category))
    else:
        cursor.execute('''
            SELECT id, title, content, category, tags, created_at 
            FROM knowledge_base 
            WHERE title LIKE ? OR content LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
    
    results = cursor.fetchall()
    conn.close()
    
    entries = []
    for row in results:
        entry_id, title, content, category, tags_json, created_at = row
        try:
            tags = json.loads(tags_json) if tags_json else []
        except:
            tags = []
        
        entries.append({
            "id": entry_id,
            "title": title,
            "content": content[:200] + "..." if len(content) > 200 else content,
            "category": category,
            "tags": tags,
            "created_at": created_at
        })
    
    return entries

@mcp.tool()
def list_documents() -> List[Dict[str, Any]]:
    """列出所有文档"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, summary, created_at FROM documents ORDER BY created_at DESC")
    results = cursor.fetchall()
    conn.close()
    
    documents = []
    for row in results:
        documents.append({
            "id": row[0],
            "filename": row[1],
            "summary": row[2],
            "created_at": row[3]
        })
    
    return documents

@mcp.tool()
def get_statistics() -> Dict[str, Any]:
    """获取系统统计信息"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 文档统计
    cursor.execute("SELECT COUNT(*) FROM documents")
    doc_count = cursor.fetchone()[0]
    
    # 知识库统计
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    kb_count = cursor.fetchone()[0]
    
    # 分类统计
    cursor.execute("SELECT category, COUNT(*) FROM knowledge_base GROUP BY category")
    category_stats = dict(cursor.fetchall())
    
    conn.close()
    
    return {
        "total_documents": doc_count,
        "total_knowledge_entries": kb_count,
        "categories": category_stats,
        "database_path": DB_PATH
    }

# 资源定义
@mcp.resource("document://{document_id}")
def get_document_resource(document_id: str) -> str:
    """获取文档资源"""
    try:
        doc_id = int(document_id)
        result = get_document_content(doc_id)
        if "error" in result:
            return result["error"]
        return f"Document: {result['filename']}\n\nContent:\n{result['content']}"
    except ValueError:
        return f"Invalid document ID: {document_id}"

@mcp.resource("knowledge://{entry_id}")
def get_knowledge_resource(entry_id: str) -> str:
    """获取知识库条目资源"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM knowledge_base WHERE id = ?", (int(entry_id),))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return f"Knowledge Entry: {result[0]}\n\nContent:\n{result[1]}"
        else:
            return f"Knowledge entry with ID {entry_id} not found"
    except ValueError:
        return f"Invalid entry ID: {entry_id}"

if __name__ == "__main__":
    print("智能文档处理与知识管理MCP服务器启动中...")
    print("支持的功能:")
    print("- 文档解析 (TXT, PDF, DOCX)")
    print("- 关键词提取")
    print("- 摘要生成")
    print("- 知识库管理")
    print("- 智能搜索")
    
    # 启动服务器
    mcp.run()