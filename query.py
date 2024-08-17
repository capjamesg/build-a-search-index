from lark import Lark, Transformer
from app import search, documents_by_title

grammar = """
start: query
query: ("(" WORD (OPERATOR WORD)* ")") | (query OPERATOR query)* | WORD
OPERATOR: "AND NOT" | "AND" | "OR"

WORD: /[a-z0-9_ ]+/

%import common.CNAME
%import common.WS
%ignore WS
"""


parser = Lark(grammar)

DOCUMENT_SEARCH_KEY = "title"


class ExpressionInterpreter(Transformer):
    """
    Reads a parsed Lark tree, evaluates each part of the tree, and returns
    documents that match the description in the tree.
    """
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
            print("Processed single string value", items[0], "\n")
            return search(items[0])
        else:
            return items[0]

    def OPERATOR(self, token):
        """
        Transforms OPERATOR tokens into their respective Python set functions.
        """
        if token == "AND":
            return set.intersection
        elif token == "OR":
            return set.union
        elif token == "AND NOT":
            return set.difference

    def start(self, items):
        """
        Lark trees need an entry point which serves as the root of the tree.

        The entry point for the transformer is `start`.

        This function tells the transformer that `start` should be treated as a query.
        """
        return self.query(items)

query = "(I love AND still) OR kiss"

def preprocess(query):
    """
    Preprocesses the query to make it compatible with the grammar.
    """
    RESERVED_TERMS = ["AND", "OR"]

    terms = query.split()
    terms = [t.lower() if t not in RESERVED_TERMS else t for t in terms]

    return " ".join(terms)

result = parser.parse(preprocess(query))

print(result.pretty())

ast = ExpressionInterpreter().transform(result)

print([doc[DOCUMENT_SEARCH_KEY] for doc in ast])
