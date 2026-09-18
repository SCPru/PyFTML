from ftml_ast import AbstractBlock
from .span import SpanBlock
from .div import DivBlock


BLOCKS_LIST: list[type[AbstractBlock]] = [
    DivBlock,
    SpanBlock
]

BLOCKS = {block.name(): block for block in BLOCKS_LIST}

