from ftml_ast import AbstractBlock


class DivBlock(AbstractBlock):
    class_name: str
    style: str

    @classmethod
    def name(cls):
        return 'div'
     