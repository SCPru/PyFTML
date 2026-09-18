from dataclasses import dataclass, field


@dataclass(slots=True)
class AstNode:
    children: list['AstNode'] = field(default_factory=list)


@dataclass(slots=True)
class DocumentRoot(AstNode):
    pass


@dataclass(slots=True)
class AbstractBlock(AstNode):
    is_starred: bool = False
    is_underscorred: bool = False

    @classmethod
    def name(cls) -> str:
        raise NotImplementedError('Abstract block has no name')
    
    @classmethod
    def has_body(cls) -> bool:
        return True