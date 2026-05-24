import ast
from typing import List, Optional, Tuple


class ASTUtils:
    @staticmethod
    def parse_safe(content: str) -> Optional[ast.AST]:
        try:
            return ast.parse(content)
        except SyntaxError:
            return None

    @staticmethod
    def get_functions(tree: ast.AST) -> List[ast.FunctionDef]:
        return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]

    @staticmethod
    def get_classes(tree: ast.AST) -> List[ast.ClassDef]:
        return [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

    @staticmethod
    def get_imports(tree: ast.AST) -> List[Tuple[int, str, str]]:
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((node.lineno, "import", alias.name))
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append((node.lineno, "from", node.module or "", alias.name))
        return imports

    @staticmethod
    def get_function_body_lines(node: ast.FunctionDef) -> List[str]:
        lines = []
        for child in ast.walk(node):
            if isinstance(child, (ast.Expr, ast.Assign, ast.Return,
                                  ast.If, ast.For, ast.While, ast.Call)):
                lines.append(type(child).__name__)
        return lines
