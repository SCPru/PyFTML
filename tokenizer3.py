from typing import List
from enum import Enum, unique
import re


WHITESPACE_CHARS = r'\s'

@unique
# Priority-ordered tokens list
class TokenType(Enum):
    Null = -1

    String = 0
    QuotedString = 1
    Whitespace = 2

    OpenComment = '[!--'
    CloseComment = '--]'

    OpenTripleBracket = '[[['
    CloseTripleBracket = ']]]'
    OpenDoubleBracket = '[['
    CloseDoubleBracket = ']]'
    OpenSingleBracket = '['
    CloseSingleBracket = ']'

    Quote = '"'

    Blockquote = '>'

    DoubleAt = '@@'
    DoubleHash = '##'

    DoublePipe = '||'

    DoubleSup = '^^'
    DoubleSub = ',,'

    OpenHTMLLiteral = '@<'
    CloseHTMLLiteral = '>@'

    OpenInlineCode = '{{'
    CloseInlineCode = '}}'

    HrBeginning = '----'
    ClearFloatBeginning = '~~~~'

    DoubleDash = '--'
    DoubleAsterisk = '**'
    DoubleSlash = '//'
    DoubleUnderline = '__'

    Equals = '='
    Pipe = '|'
    Asterisk = '*'
    Hash = '#'
    Plus = '+'
    Newline = '\n'
    Slash = '/'
    Backslash = '\\'
    Tilde = '~'
    Underline = '_'


class Token:
    def __init__(self, type: TokenType, start: int, end: int, source: str):
        self.type = type
        self.start = start
        self.end = end
        self.source = source

    @property
    def raw(self):
        return self.source[self.start:self.end]

    def __repr__(self):
        return '<Token type=%s, raw=%s>' % (self.type.name, repr(self.raw))


class Tokenizer:
    def __init__(self):
        self.rules = {rule.value: rule for rule in TokenType if not isinstance(rule.value, int)}
        self.token_regex = re.compile('|'.join(re.escape(rule.value) for rule in TokenType if not isinstance(rule.value, int)) + f'|[{WHITESPACE_CHARS}]+')

    def tokenize(self, source: str) -> List[Token]:
        tokens: List[Token] = []
        last_end = 0

        for match in self.token_regex.finditer(source):
            start, end = match.span()
            if start > last_end:
                tokens.append(Token(TokenType.String, last_end, start, source))
            group = match.group()
            token_type = self.rules.get(group, TokenType.Whitespace)
            tokens.append(Token(token_type, start, end, source))
            last_end = end

        if last_end < len(source):
            tokens.append(Token(TokenType.String, last_end, len(source), source))

        return tokens