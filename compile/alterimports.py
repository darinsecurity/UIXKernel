import ast

class ImportTransformer(ast.NodeTransformer):
    def visit_Import(self, node):
        new_nodes = []
        for alias in node.names:
            name = alias.name
            new_node = ast.Assign(
                targets=[ast.Name(id=name, ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id='__import__', ctx=ast.Load()),
                    args=[ast.Constant(value=name)],
                    keywords=[]
                )
            )
            # Set lineno and col_offset for the new node
            new_node.lineno = node.lineno
            new_node.col_offset = node.col_offset
            new_node.end_lineno = node.end_lineno
            new_node.end_col_offset = node.end_col_offset
            new_nodes.append(new_node)
        return new_nodes

    def visit_ImportFrom(self, node):
        module = node.module
        new_nodes = []
        for alias in node.names:
            name = alias.name
            asname = alias.asname if alias.asname else name
            new_node = ast.Assign(
                targets=[ast.Name(id=asname, ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id='__import__', ctx=ast.Load()),
                    args=[ast.Constant(value=module)],
                    keywords=[]
                )
            )
            # Set lineno and col_offset for the new node
            new_node.lineno = node.lineno
            new_node.col_offset = node.col_offset
            new_node.end_lineno = node.end_lineno
            new_node.end_col_offset = node.end_col_offset
            new_nodes.append(new_node)
        return new_nodes

def replace_imports(source_code):
    tree = ast.parse(source_code)
    transformer = ImportTransformer()
    transformed_tree = transformer.visit(tree)
    ast.fix_missing_locations(transformed_tree)  # Ensure the new tree has all necessary locations
    return ast.unparse(transformed_tree)