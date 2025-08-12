"""
代码分析工具模块
"""

import ast
import os
import subprocess
import json
from typing import Dict, List, Any, Optional
from pathlib import Path


class CodeAnalyzer:
    """代码分析器"""
    
    def __init__(self):
        self.supported_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx'}
    
    def analyze_code_quality(self, file_path: str) -> Dict[str, Any]:
        """分析代码质量"""
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
        
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.py':
            return self._analyze_python_file(file_path)
        elif file_ext in {'.js', '.ts', '.jsx', '.tsx'}:
            return self._analyze_javascript_file(file_path)
        else:
            return {"error": f"Unsupported file type: {file_ext}"}
    
    def _analyze_python_file(self, file_path: str) -> Dict[str, Any]:
        """分析Python文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # AST分析
            tree = ast.parse(content)
            
            # 基础指标
            metrics = {
                "file_path": file_path,
                "language": "python",
                "lines_of_code": len(content.splitlines()),
                "functions": self._count_functions(tree),
                "classes": self._count_classes(tree),
                "complexity_score": self._calculate_complexity(tree),
                "issues": []
            }
            
            # 代码质量检查
            issues = self._check_python_issues(content, tree)
            metrics["issues"] = issues
            metrics["quality_score"] = max(0, 100 - len(issues) * 5)
            
            return metrics
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_javascript_file(self, file_path: str) -> Dict[str, Any]:
        """分析JavaScript/TypeScript文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 基础指标
            metrics = {
                "file_path": file_path,
                "language": "javascript/typescript",
                "lines_of_code": len(content.splitlines()),
                "functions": self._count_js_functions(content),
                "complexity_score": self._estimate_js_complexity(content),
                "issues": []
            }
            
            # 简单的代码质量检查
            issues = self._check_js_issues(content)
            metrics["issues"] = issues
            metrics["quality_score"] = max(0, 100 - len(issues) * 5)
            
            return metrics
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _count_functions(self, tree: ast.AST) -> int:
        """计算Python函数数量"""
        return len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
    
    def _count_classes(self, tree: ast.AST) -> int:
        """计算Python类数量"""
        return len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
    
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """计算圈复杂度（简化版）"""
        complexity = 1  # 基础复杂度
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _check_python_issues(self, content: str, tree: ast.AST) -> List[Dict[str, Any]]:
        """检查Python代码问题"""
        issues = []
        lines = content.splitlines()
        
        # 检查长行
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append({
                    "type": "style",
                    "severity": "warning",
                    "line": i,
                    "message": f"Line too long ({len(line)} > 120 characters)"
                })
        
        # 检查函数复杂度
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_complexity = self._calculate_function_complexity(node)
                if func_complexity > 10:
                    issues.append({
                        "type": "complexity",
                        "severity": "warning",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' is too complex (complexity: {func_complexity})"
                    })
        
        # 检查未使用的导入（简化版）
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        if len(imports) > 20:
            issues.append({
                "type": "maintainability",
                "severity": "info",
                "line": 1,
                "message": f"Too many imports ({len(imports)}), consider refactoring"
            })
        
        return issues
    
    def _calculate_function_complexity(self, func_node: ast.FunctionDef) -> int:
        """计算单个函数的复杂度"""
        complexity = 1
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
        return complexity
    
    def _count_js_functions(self, content: str) -> int:
        """计算JavaScript函数数量（简化版）"""
        import re
        function_patterns = [
            r'function\s+\w+',
            r'\w+\s*:\s*function',
            r'=>',
            r'function\s*\('
        ]
        
        count = 0
        for pattern in function_patterns:
            count += len(re.findall(pattern, content))
        
        return count
    
    def _estimate_js_complexity(self, content: str) -> int:
        """估算JavaScript复杂度"""
        import re
        complexity_keywords = ['if', 'else', 'while', 'for', 'switch', 'case', 'try', 'catch']
        
        complexity = 1
        for keyword in complexity_keywords:
            complexity += len(re.findall(rf'\b{keyword}\b', content))
        
        return complexity
    
    def _check_js_issues(self, content: str) -> List[Dict[str, Any]]:
        """检查JavaScript代码问题"""
        issues = []
        lines = content.splitlines()
        
        # 检查长行
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append({
                    "type": "style",
                    "severity": "warning",
                    "line": i,
                    "message": f"Line too long ({len(line)} > 120 characters)"
                })
        
        # 检查console.log（生产环境不应该有）
        import re
        console_logs = re.finditer(r'console\.log', content)
        for match in console_logs:
            line_num = content[:match.start()].count('\n') + 1
            issues.append({
                "type": "maintainability",
                "severity": "info",
                "line": line_num,
                "message": "console.log found - consider removing for production"
            })
        
        return issues

    def analyze_project_structure(self, project_path: str) -> Dict[str, Any]:
        """分析项目结构"""
        if not os.path.exists(project_path):
            return {"error": f"Project path not found: {project_path}"}
        
        structure = {
            "project_path": project_path,
            "total_files": 0,
            "code_files": 0,
            "languages": {},
            "directories": [],
            "files_by_type": {}
        }
        
        for root, dirs, files in os.walk(project_path):
            # 跳过隐藏目录和常见的忽略目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'node_modules', '__pycache__', 'venv', 'env'}]
            
            rel_root = os.path.relpath(root, project_path)
            if rel_root != '.':
                structure["directories"].append(rel_root)
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                structure["total_files"] += 1
                file_ext = Path(file).suffix.lower()
                
                # 统计文件类型
                if file_ext in structure["files_by_type"]:
                    structure["files_by_type"][file_ext] += 1
                else:
                    structure["files_by_type"][file_ext] = 1
                
                # 统计编程语言
                if file_ext in self.supported_extensions:
                    structure["code_files"] += 1
                    lang = self._get_language_from_extension(file_ext)
                    if lang in structure["languages"]:
                        structure["languages"][lang] += 1
                    else:
                        structure["languages"][lang] = 1
        
        return structure
    
    def _get_language_from_extension(self, ext: str) -> str:
        """根据文件扩展名获取编程语言"""
        mapping = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React JSX',
            '.tsx': 'React TSX'
        }
        return mapping.get(ext, 'Unknown')