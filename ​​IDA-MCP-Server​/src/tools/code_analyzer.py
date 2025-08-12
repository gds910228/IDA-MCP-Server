"""
代码分析工具模块
"""

import ast
import os
import subprocess
import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
"""
代码分析工具模块
"""

"""
代码分析工具模块
"""

import ast
import os
import subprocess
import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path


class CodeAnalyzer:
    """代码分析器"""
    
    def __init__(self):
        self.supported_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx'}
    
    def _resolve_file_path(self, file_path: str) -> str:
        """解析文件路径，支持相对路径和绝对路径"""
        if os.path.isabs(file_path):
            return file_path
        
        # 获取当前工作目录
        cwd = os.getcwd()
        
        # 定义可能的项目根目录（按优先级排序）
        possible_project_roots = [
            # 1. 已知的项目路径（最高优先级）
            r'D:\WorkProjects\AI\MCP\IDA-MCP-Server',
            r'd:\WorkProjects\AI\MCP\IDA-MCP-Server',
            # 2. 从当前目录向上查找包含main.py的目录
            self._find_project_root_with_main_py(cwd),
            # 3. 用户目录下的项目路径
            os.path.join(os.path.expanduser('~'), 'WorkProjects', 'AI', 'MCP', 'IDA-MCP-Server'),
            # 4. 当前工作目录
            cwd
        ]
        
        # 找到第一个有效的项目根目录
        project_root = None
        for root in possible_project_roots:
            if root and os.path.exists(root):
                # 验证这确实是一个项目目录（包含main.py或src目录）
                if (os.path.exists(os.path.join(root, 'main.py')) or 
                    os.path.exists(os.path.join(root, 'src')) or
                    root == cwd):
                    project_root = root
                    break
        
        # 如果还是没找到，使用当前工作目录
        if not project_root:
            project_root = cwd
        
        # 尝试多种路径解析方式（按优先级排序）
        possible_paths = [
            # 1. 相对于已知项目根目录
            os.path.join(project_root, file_path),
            # 2. 去掉开头的 "./" 或 ".\"
            os.path.join(project_root, file_path.lstrip('./\\')),
            # 3. 直接使用相对路径转绝对路径（基于当前工作目录）
            os.path.abspath(file_path),
            # 4. 相对于当前工作目录
            os.path.join(cwd, file_path),
            # 5. 在项目根目录的src子目录中查找
            os.path.join(project_root, 'src', file_path) if not file_path.startswith('src') else os.path.join(project_root, file_path),
            # 6. 直接在项目根目录查找文件名
            os.path.join(project_root, os.path.basename(file_path))
        ]
        
        # 找到第一个存在的路径
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # 如果都不存在，返回基于项目根目录的路径（即使不存在，也便于调试）
        return os.path.join(project_root, file_path)
    
    def _find_project_root_with_main_py(self, start_dir: str) -> Optional[str]:
        """从指定目录向上查找包含main.py的目录"""
        current_dir = start_dir
        for _ in range(10):  # 最多向上查找10级目录
            if os.path.exists(os.path.join(current_dir, 'main.py')):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:  # 已到根目录
                break
            current_dir = parent_dir
        return None
    
    def _get_debug_paths(self, file_path: str) -> List[str]:
        """获取所有尝试的路径用于调试"""
        cwd = os.getcwd()
        possible_project_roots = [
            r'D:\WorkProjects\AI\MCP\IDA-MCP-Server',
            r'd:\WorkProjects\AI\MCP\IDA-MCP-Server',
            self._find_project_root_with_main_py(cwd),
            os.path.join(os.path.expanduser('~'), 'WorkProjects', 'AI', 'MCP', 'IDA-MCP-Server'),
            cwd
        ]
        
        debug_paths = []
        for root in possible_project_roots:
            if root:
                debug_paths.extend([
                    os.path.join(root, file_path),
                    os.path.join(root, file_path.lstrip('./\\')),
                    os.path.join(root, 'src', file_path),
                    os.path.join(root, os.path.basename(file_path))
                ])
        
        debug_paths.extend([
            os.path.abspath(file_path),
            os.path.join(cwd, file_path)
        ])
        
        return debug_paths
    
    def analyze_code_quality(self, file_path: str) -> Dict[str, Any]:
        """分析代码质量"""
        # 处理相对路径和绝对路径
        original_path = file_path
        resolved_path = self._resolve_file_path(file_path)
        
        # 添加详细的调试信息
        debug_info = {
            "original_path": original_path,
            "current_working_directory": os.getcwd(),
            "resolved_path": resolved_path,
            "file_exists": os.path.exists(resolved_path),
            "tried_paths": self._get_debug_paths(file_path)
        }
        
        if not os.path.exists(resolved_path):
            return {
                "error": f"File not found: {resolved_path}",
                **debug_info
            }
        
        file_path = resolved_path
        
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