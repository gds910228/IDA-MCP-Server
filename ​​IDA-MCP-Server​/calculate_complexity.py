#!/usr/bin/env python3
"""
代码复杂度计算工具
"""

import ast
import os
import sys
from typing import Dict, List, Any

class ComplexityCalculator:
    """代码复杂度计算器"""
    
    def __init__(self):
        self.complexity_score = 0
        self.functions = []
        self.classes = []
    
    def visit_node(self, node):
        """访问AST节点并计算复杂度"""
        if isinstance(node, ast.FunctionDef):
            func_complexity = self.calculate_function_complexity(node)
            self.functions.append({
                'name': node.name,
                'complexity': func_complexity,
                'line': node.lineno
            })
            self.complexity_score += func_complexity
            
        elif isinstance(node, ast.ClassDef):
            self.classes.append({
                'name': node.name,
                'line': node.lineno,
                'methods': []
            })
            
        # 递归访问子节点
        for child in ast.iter_child_nodes(node):
            self.visit_node(child)
    
    def calculate_function_complexity(self, func_node):
        """计算函数的圈复杂度"""
        complexity = 1  # 基础复杂度
        
        for node in ast.walk(func_node):
            # 条件语句增加复杂度
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            # 异常处理增加复杂度
            elif isinstance(node, (ast.ExceptHandler, ast.Try)):
                complexity += 1
            # 逻辑运算符增加复杂度
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            # 三元运算符增加复杂度
            elif isinstance(node, ast.IfExp):
                complexity += 1
            # 列表/字典推导式增加复杂度
            elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
                complexity += 1
        
        return complexity
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """分析文件的复杂度"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析AST
            tree = ast.parse(content)
            
            # 重置计数器
            self.complexity_score = 0
            self.functions = []
            self.classes = []
            
            # 访问所有节点
            self.visit_node(tree)
            
            # 计算代码行数
            lines_of_code = len([line for line in content.split('\n') if line.strip() and not line.strip().startswith('#')])
            
            # 确定复杂度等级
            if self.complexity_score < 10:
                complexity_level = "low"
            elif self.complexity_score < 20:
                complexity_level = "medium"
            else:
                complexity_level = "high"
            
            return {
                "file_path": file_path,
                "complexity_score": self.complexity_score,
                "complexity_level": complexity_level,
                "functions_count": len(self.functions),
                "classes_count": len(self.classes),
                "lines_of_code": lines_of_code,
                "functions": self.functions,
                "classes": self.classes,
                "analysis_summary": {
                    "average_function_complexity": round(self.complexity_score / max(len(self.functions), 1), 2),
                    "most_complex_function": max(self.functions, key=lambda x: x['complexity']) if self.functions else None,
                    "recommendations": self.get_recommendations()
                }
            }
            
        except Exception as e:
            return {
                "error": f"分析文件时出错: {str(e)}",
                "file_path": file_path
            }
    
    def get_recommendations(self) -> List[str]:
        """获取优化建议"""
        recommendations = []
        
        if self.complexity_score > 20:
            recommendations.append("代码复杂度较高，建议重构以降低复杂度")
        
        high_complexity_functions = [f for f in self.functions if f['complexity'] > 10]
        if high_complexity_functions:
            recommendations.append(f"发现 {len(high_complexity_functions)} 个高复杂度函数，建议拆分")
        
        if len(self.functions) > 20:
            recommendations.append("函数数量较多，建议考虑模块化")
        
        if not recommendations:
            recommendations.append("代码复杂度在合理范围内")
        
        return recommendations

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python calculate_complexity.py <文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        sys.exit(1)
    
    calculator = ComplexityCalculator()
    result = calculator.analyze_file(file_path)
    
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()