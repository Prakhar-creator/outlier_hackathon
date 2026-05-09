import ast


class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        # Base complexity starts at 1
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        # Each boolean operator increases complexity
        # a and b or c → 2 operators → +2
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        # Ternary expression: x if cond else y
        self.complexity += 1
        self.generic_visit(node)


def compute_function_complexities(source_code: str) -> list[int]:
    tree = ast.parse(source_code)
    complexities = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visitor = ComplexityVisitor()
            visitor.visit(node)
            complexities.append(visitor.complexity)

    return complexities