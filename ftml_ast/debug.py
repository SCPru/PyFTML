from ftml_ast import AstNode


def print_ast(ast: AstNode, indent: int = 0):
    print(' ' * indent + str(ast.__class__.__name__))
    for child in ast.children:
        print(child, indent + 2)