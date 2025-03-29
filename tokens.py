from enum import Enum


class Token(Enum):
    WHILE = (1, "while")
    VAR = (2, "var")
    TO = (3, "to")
    THEN = (4, "then")
    STRING = (5, "string")
    REAL = (6, "real")
    READ = (7, "read")
    PROGRAM = (8, "program")
    PROCEDURE = (9, "procedure")
    PRINT = (10, "print")
    INTEGER = (14, "integer")
    IF = (15, "if")
    FOR = (17, "for")
    END = (18, "end")
    ELSE = (19, "else")
    DO = (20, "do")
    CONST = (21, "const")
    BEGIN = (22, "begin")
    GREATER_EQUAL = (24, ">=")
    GREATER = (25, ">")
    EQUAL = (26, "=")
    NOT_EQUAL = (27, "<>")
    LESS_EQUAL = (28, "<=")
    LESS = (29, "<")
    PLUS = (30, "+")
    SEMICOLON = (31, ";")
    ASSIGN = (32, ":=")
    COLON = (33, ":")
    DIVIDE = (34, "/")
    DOT = (35, ".")
    COMMA = (36, ",")
    MULTIPLY = (37, "*")
    CLOSE_PAREN = (38, ")")
    OPEN_PAREN = (39, "(")
    OPEN_BRACE = (40, "{")
    CLOSE_BRACE = (41, "}")
    MINUS = (42, "-")
    DOLLAR = (43, "$")
    QUOTE = (44, "'")
    QUOTE_DOUBLE = (45, '"')

    def __init__(self, code, lexeme):
        self.code = code
        self.lexeme = lexeme

    @classmethod
    def getByLexeme(cls, lexeme):
        for token in cls:
            if token.lexeme == lexeme:
                return token
        return None  # Retorna None se não encontrar

    @classmethod
    def getVString(cls):
        return (23, "vstring");

    @classmethod
    def getLiteral(cls):
        return (13, "literal");

    @classmethod
    def getIdent(cls):
        return (16, "ident");

    @classmethod
    def getNReal(cls):
        return (11, "nreal");
    
    @classmethod
    def getNInt(cls):
        return (12, "nint");
