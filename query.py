from lark import Lark, Transformer
from lark.visitors import Interpreter, Visitor, Visitor_Recursive
from .search_engine import search, documents_by_title

grammar = """
start: query
query: ("(" WORD (OPERATOR WORD)* ")") | (query OPERATOR query)* | WORD (WORD)*
OPERATOR: "AND NOT" | "AND" | "OR"

WORD: /[a-zA-Z0-9_]+/

%import common.WS
%ignore WS
"""

parser = Lark(grammar)

DOCUMENT_SEARCH_KEY = "title"


class ExpressionInterpreter(Transformer):
    def query(self, items):
        if len(items) > 1:
            if isinstance(items[0], str):
                left = search(items[0])
            else:
                left = items[0]

            if isinstance(items[2], str):
                right = search(items[2])
            else:
                right = items[2]

            operand = items[1]

            left_doc_keys = set([doc[DOCUMENT_SEARCH_KEY] for doc in left])
            right_doc_keys = set([doc[DOCUMENT_SEARCH_KEY] for doc in right])

            doc_keys_after_query = operand(left_doc_keys, right_doc_keys)

            result = [documents_by_title[title] for title in doc_keys_after_query]

            return result
        elif len(items) == 1 and isinstance(items[0], str):
            return search(items[0])
        else:
            return items[0]

    def WORD(self, items):
        return items

    def OPERATOR(self, token):
        if token == "AND":
            return set.intersection
        elif token == "OR":
            return set.union
        elif token == "AND NOT":
            return set.difference

    def start(self, items):
        return self.query(items)


result = parser.parse("(I AND NOT still)")

ast = ExpressionInterpreter().transform(result)

print([doc["title"] for doc in ast])
