import ast

def clean_code(lines):
   return remove_comments_multiple(lines)


def remove_comments_multiple(source):
    """
    This function takes Python source code and removes comments from it.

    :param source: A string representing Python source code
    :return: A string with the comments removed
    """
    class CommentRemover(ast.NodeTransformer):
        def visit(self, node):
            if hasattr(node, 'body'):
                new_body = []
                for item in node.body:
                    if not (isinstance(item, ast.Expr) and isinstance(item.value, ast.Constant) and isinstance(item.value.value, str)):
                        new_body.append(item)
                node.body = new_body
            return self.generic_visit(node)

    tree = ast.parse(source)
    tree = CommentRemover().visit(tree)
    ast.fix_missing_locations(tree)

    return ast.unparse(tree)



def remove_comments(line):
    """
    This function takes a line of Python code and removes comments from it.

    :param line: A string representing a line of Python code
    :return: A string with the comments removed
    """
    # Parse the line of code into an AST
    node = ast.parse(line)

    # Extract the source code from the AST
    code_without_comments = ast.unparse(node)

    # Strip any trailing whitespace
    return code_without_comments.rstrip()
