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
    NREAL = (11, "nreal")
    NINT = (12, "nint")
    LITERAL = (13, "literal")
    INTEGER = (14, "integer")
    IF = (15, "if")
    IDENT = (16, "ident")
    FOR = (17, "for")
    END = (18, "end")
    ELSE = (19, "else")
    DO = (20, "do")
    CONST = (21, "const")
    BEGIN = (22, "begin")
    VSTRING = (23, "vstring")
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
    QUOTE = (101, "'")
    QUOTE_DOUBLE = (102, '"')

    PROGRAMA = (45, "PROGRAMA")
    DECLARACOES = (46, "DECLARACOES")
    BLOCO = (47, "BLOCO")
    CONSTANTES = (48, "CONSTANTES")
    VARIAVEIS = (49, "VARIAVEIS")
    PROCEDIMENTOS = (50, "PROCEDIMENTOS")
    COMANDOS = (51, "COMANDOS")
    LISTAVARIAVEIS = (52, "LISTAVARIAVEIS")
    TIPO = (53, "TIPO")
    LDVAR = (54, "LDVAR")
    REPIDENT = (55, "REPIDENT")
    PARAMETROS = (56, "PARAMETROS")
    REPARAMETROS = (57, "REPARAMETROS")
    COMANDO = (58, "COMANDO")
    ITEMSAIDA = (59, "ITEMSAIDA")
    REPITEM = (60, "REPITEM")
    EXPRESSAO = (61, "EXPRESSAO")
    TERMO = (62, "TERMO")
    EXPR = (63, "EXPR")
    FATOR = (64, "FATOR")
    TER = (65, "TER")
    EXPRELACIONAL = (66, "EXPRELACIONAL")
    ELSEOPC = (67, "ELSEOPC")
    OPREL = (68, "OPREL")
    CHAMADAPROC = (69, "CHAMADAPROC")
    LISTAPARAMETROS = (70, "LISTAPARAMETROS")
    PAR = (71, "PAR")
    REPPAR = (72, "REPPAR")

    def __init__(self, code, lexeme):
        self.code = code
        self.lexeme = lexeme

    @classmethod
    def getByLexeme(cls, lexeme):
        for token in cls:
            if token.code == 16 or token.code == 11 or token.code == 12 or token.code == 13 or token.code == 23:
                continue
            if token.lexeme == lexeme:
                return token
        return None  # Retorna None se não encontrar

    @classmethod
    def getByCode(cls, code):
        for token in cls:
            if token.code == code:
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
