from typing import List
from enum import Enum, auto, unique
from dataclasses import dataclass
import re


WHITESPACE_CHARS = r'\s'

@unique
class TokenType(Enum):
    STRING = auto()
    WHITESPACE = auto()

    OPEN_COMMENT = auto()
    CLOSE_COMMENT = auto()

    OPEN_TRIPLE_BRACKET = auto()
    CLOSE_TRIPLE_BRACKET = auto()

    OPEN_DOUBLE_BRACKET = auto()
    CLOSE_DOUBLE_BRACKET = auto()

    OPEN_SINGLE_BRACKET = auto()
    CLOSE_SINGLE_BRACKET = auto()

    QUOTE = auto()
    BLOCKQUOTE = auto()

    DOUBLE_AT = auto()
    DOUBLE_HASH = auto()
    DOUBLE_PIPE = auto()

    DOUBLE_SUP = auto()
    DOUBLE_SUB = auto()

    OPEN_HTML_LITERAL = auto()
    CLOSE_HTML_LITERAL = auto()

    OPEN_INLINE_CODE = auto()
    CLOSE_INLINE_CODE = auto()

    HR_BEGINNING = auto()
    CLEAR_FLOAT_BEGINNING = auto()

    DOUBLE_DASH = auto()
    DOUBLE_ASTERISK = auto()
    DOUBLE_SLASH = auto()
    DOUBLE_UNDERLINE = auto()

    EQUALS = auto()
    PIPE = auto()
    ASTERISK = auto()
    HASH = auto()
    PLUS = auto()

    NEWLINE = auto()

    SLASH = auto()
    BACKSLASH = auto()
    TILDE = auto()
    UNDERLINE = auto()


TOKEN_LITERALS = {
    '[!--': TokenType.OPEN_COMMENT,
    '--]': TokenType.CLOSE_COMMENT,

    '[[[': TokenType.OPEN_TRIPLE_BRACKET,
    ']]]': TokenType.CLOSE_TRIPLE_BRACKET,

    '[[': TokenType.OPEN_DOUBLE_BRACKET,
    ']]': TokenType.CLOSE_DOUBLE_BRACKET,

    '[': TokenType.OPEN_SINGLE_BRACKET,
    ']': TokenType.CLOSE_SINGLE_BRACKET,

    '"': TokenType.QUOTE,
    '>': TokenType.BLOCKQUOTE,

    '@@': TokenType.DOUBLE_AT,
    '##': TokenType.DOUBLE_HASH,
    '||': TokenType.DOUBLE_PIPE,

    '^^': TokenType.DOUBLE_SUP,
    ',,': TokenType.DOUBLE_SUB,

    '@<': TokenType.OPEN_HTML_LITERAL,
    '>@': TokenType.CLOSE_HTML_LITERAL,

    '{{': TokenType.OPEN_INLINE_CODE,
    '}}': TokenType.CLOSE_INLINE_CODE,

    '----': TokenType.HR_BEGINNING,
    '~~~~': TokenType.CLEAR_FLOAT_BEGINNING,

    '--': TokenType.DOUBLE_DASH,
    '**': TokenType.DOUBLE_ASTERISK,
    '//': TokenType.DOUBLE_SLASH,
    '__': TokenType.DOUBLE_UNDERLINE,

    '=': TokenType.EQUALS,
    '|': TokenType.PIPE,
    '*': TokenType.ASTERISK,
    '#': TokenType.HASH,
    '+': TokenType.PLUS,

    '\n': TokenType.NEWLINE,

    '/': TokenType.SLASH,
    '\\': TokenType.BACKSLASH,
    '~': TokenType.TILDE,
    '_': TokenType.UNDERLINE,
}


_LITERAL_PATTERN = '|'.join(
    re.escape(literal)
    for literal in sorted(
        TOKEN_LITERALS,
        key=len,
        reverse=True,
    )
)

TOKEN_REGEX = re.compile(
    rf'(?:{_LITERAL_PATTERN})|[^\S\n]+'
)

@dataclass(slots=True)
class TokenStream:
    source: str
    tokens: list[Token]

    def raw(self, token: Token) -> str:
        return self.source[token.start:token.end]


@dataclass(slots=True, frozen=True)
class Token:
    token_type: TokenType
    start: int
    end: int


class Tokenizer:
    def tokenize(self, source: str) -> TokenStream:
        tokens: List[Token] = []
        last_end = 0

        for match in TOKEN_REGEX.finditer(source):
            start, end = match.span()
            if start > last_end:
                tokens.append(Token(TokenType.STRING, last_end, start))
            group = match.group()
            token_type = TOKEN_LITERALS.get(group, TokenType.WHITESPACE)
            tokens.append(Token(token_type, start, end))
            last_end = end

        if last_end < len(source):
            tokens.append(Token(TokenType.STRING, last_end, len(source)))

        return TokenStream(source, tokens)