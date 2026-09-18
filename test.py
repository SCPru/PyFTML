from ftml_ast.debug import print_ast
from tokenizer3 import Tokenizer
from parser import Parser

with open('test.ftml') as f:
    text = f.read()

# t = Tokenizer()

# stream = t.tokenize(text)

# for token in stream.tokens:
#     print(f'{token.token_type:<30} | {repr(stream.raw(token))}')

parser = Parser()
root = parser.parse(text)
print_ast(root)