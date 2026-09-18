from ftml_ast import AbstractBlock


class SpanBlock(AbstractBlock):
    class_name: str
    style: str

    @classmethod
    def name(cls):
        return 'span'
     