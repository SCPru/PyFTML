from typing import Optional, Union

from ftml_ast import AstNode, DocumentRoot
from ftml_ast.blocks import BLOCKS
from ftml_ast.blocks import AbstractBlock
from tokenizer3 import Token, TokenStream, TokenType, Tokenizer


class Parser:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.position = 0
        self.token_stream: TokenStream
        self.all_blocks = BLOCKS

    def advance(self) -> Token:
        if self.position >= len(self.token_stream.tokens):
            raise ValueError() # fuck
        token = self.token_stream.tokens[self.position]
        self.position += 1
        return token
    
    def peek(self) -> Token:
        return self.token_stream.tokens[self.position]

    def parse(self, text: str) -> DocumentRoot:
        self.token_stream = self.tokenizer.tokenize(text)
        blocks: list[AstNode] = []

        while self.position < len(self.token_stream.tokens):
            next_block = self.parse_block()
            blocks.append(next_block)

        return DocumentRoot(blocks)
    
    def _skip_to_token(self, token_type: TokenType):
        token = self.token_stream.tokens[self.position]
        while token.token_type != token_type:
            token = self.advance()
            if token is None:
                break

    def _skip_whitespace(self):
        token = self.token_stream.tokens[self.position]
        while token.token_type == TokenType.WHITESPACE:
            token = self.advance()
            if token is None:
                break

    def _fuck_if_not(self, token: Optional[Token], token_type: Union[TokenType, list[TokenType]], throw_error: bool=True):
        if isinstance(token_type, list):
            if not token or token.token_type not in token_type:
                if throw_error:
                    raise ValueError() # fuck
                return False
        if not token or token.token_type != token_type:
            raise ValueError() # fuck
        return True

    def _parse_arguments(self) -> dict[str, str]:
        self._skip_whitespace()
        kwargs = {}

        while token := self.advance():
            self._fuck_if_not(token := self.advance(), TokenType.STRING)
            key = self.token_stream.raw(token)
            self._fuck_if_not(self.advance(), TokenType.EQUALS)
            self._fuck_if_not(self.advance(), TokenType.QUOTE)
            self._fuck_if_not(token := self.advance(), TokenType.STRING)
            value = self.token_stream.raw(token)
            self._fuck_if_not(self.advance(), TokenType.QUOTE)

            kwargs.update({key: value})
        
        return kwargs

    def parse_block_open(self):
        self._skip_to_token(TokenType.OPEN_DOUBLE_BRACKET)
        self.advance()
        self._skip_whitespace()

        self._fuck_if_not(
            block := self.advance(),
            [TokenType.STRING, TokenType.ASTERISK]
        )

        is_starred = False
        if block.token_type == TokenType.ASTERISK:
            is_starred = True
            self._skip_whitespace()
            block = self.advance()
            if not block:
                raise ValueError() #fuck

        self._fuck_if_not(block, TokenType.STRING)

        block_cls = BLOCKS.get(self.token_stream.raw(block))
        if not block_cls:
            raise ValueError() #fuck

        kwargs = self._parse_arguments()

        self._skip_whitespace()
        self._fuck_if_not(block, TokenType.CLOSE_DOUBLE_BRACKET)

        return block_cls(
            is_starred=is_starred,
            is_underscorred=False,
            children=[],
            **kwargs
        )

    def parse_block_close(self, block_name: str) -> bool:
        try:
            self._fuck_if_not(self.advance(), TokenType.OPEN_DOUBLE_BRACKET)
            self._skip_whitespace()
            self._fuck_if_not(self.advance(), TokenType.CLOSE_DOUBLE_BRACKET)
            return True
        except:
            return False
    
    def parse_block(self) -> AbstractBlock:
        block_open = self.parse_block_open()

        if block_open.has_body() and self.parse_block_close(block_open.name()):
            pass

        return block_open


if __name__ == '__main__':
    pass