from enum import Enum
from tokens import Token as enumToken


class Producoes(Enum):
    PROGRAMA = (1, [8,16,31,46,47,35])
    DECLARACOES = (2, [48,49,50])
    CONSTANTES1 = (3, [21, 16, 26, 12, 31, 48])
    CONSTANTES2 = (4, None)
    VARIAVEIS = (5, [2, 52, 33, 53, 31, 54])
    LISTAVARIAVEIS = (6, [16, 55])
    REPIDENT1 = (7, None)
    REPIDENT2 = (8, [36, 16, 55])
    LDVAR1 = (9, [52, 33, 53, 31, 54])
    LDVAR2 = (10, None)
    TIPO1 = (11, [14])
    TIPO2 = (12, [6])
    TIPO3 = (13, [5])
    PROCEDIMENTOS1 = (14, [9, 16, 56, 31, 47, 31, 50])
    PROCEDIMENTOS2 = (15, None)
    PARAMETROS1 = (16, [39, 52, 33, 53, 57, 38])
    PARAMETROS2 = (17, None)
    REPARAMETROS1 = (18, [36, 52, 33, 53, 57])
    REPARAMETROS2 = (19, None)
    BLOCO = (20, [22, 51, 18])
    COMANDOS1 = (21, [58, 31, 51])
    COMANDOS2 = (22, None)
    COMANDO1 = (23, [10, 40, 59, 60, 41])
    ITEMSAIDA = (24, [61])
    REPITEM1 = (25, None)
    REPITEM2 = (26, [36, 59, 60])
    EXPRESSAO = (27, [62, 63])
    EXPR1 = (28, [30, 62, 63])
    EXPR2 = (29, [42, 62, 63])
    EXPR3 = (30, None)
    TERMO = (31, [64, 65])
    TER1 = (32, [37, 62, 63])
    TER2 = (33, [34, 62, 63])
    TER3 = (34, None)
    FATOR1 = (35, [39, 61, 38])
    FATOR2 = (36, [16])
    FATOR3 = (37, [12])
    FATOR4 = (38, [11])
    FATOR5 = (39, [13])
    FATOR6 = (40, [23])
    COMANDO2 = (41, [15, 66, 4, 47, 67])
    EXPRELACIONAL = (42, [61, 68, 61])
    OPREL1 = (43, [26])
    OPREL2 = (44, [27])
    OPREL3 = (45, [29])
    OPREL4 = (46, [25])
    OPREL5 = (47, [28])
    OPREL6 = (48, [24])
    ELSEOPC1 = (49, [19, 47])
    ELSEOPC2 = (50, None)
    COMANDO3 = (51, [16, 69])
    COMANDO4 = (52, [17, 16, 32, 61, 3, 61, 20, 47])
    CHAMADAPROC1 = (53, [70])
    CHAMADAPROC2 = (54, [32, 61])
    LISTAPARAMETROS1 = (55, [39, 71, 72, 38])
    LISTAPARAMETROS2 = (56, None)
    PAR1 = (57, [16])
    PAR2 = (58, [12])
    PAR3 = (59, [11])
    PAR4 = (60, [23])
    REPPAR1 = (61, [36, 71, 72])
    REPPAR2 = (62, None)
    COMANDO5 = (63, [1, 66, 20, 47])
    COMANDO6 = (64, [7, 39, 16, 38])
    PAR5 = (65, [13])


    def __init__(self, code, cpd):
        self.code = code
        self.cpd = cpd

    @classmethod
    def getByCode(cls, code):
        for producao in cls:
            if producao.code == code:
                return producao
        return None 
    
    @classmethod
    def escreverGramatica(cls):
        for producao in cls:
            text = "";
            if producao.cpd is not None:
                for i in range(len(producao.cpd)):
                    if(enumToken.getByCode(producao.cpd[i]) is not None):
                        text += enumToken.getByCode(producao.cpd[i]).lexeme + " "
                    elif(producao.cpd[i] == 16):
                        text += "ident "
            else:
                text = "î"
            print(producao.name + " -> " + text)
            