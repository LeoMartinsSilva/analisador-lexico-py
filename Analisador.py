import numpy as np
from tokens import Token as enumToken

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def analisarArquivo(nomeArquivo):
    with open(nomeArquivo, 'r', encoding="UTF-8") as arquivo:
        conteudo = arquivo.read()
        analisarPalavra(conteudo)

def analisarPalavra(palavra):
    lexema = '';
    tokens = []
    lexemas = []
    delimitadores = ['{', '}', ';', '(', ')', '\'', '\"', ',', ':', '=', '!', '<', '>', '+', '-', '*', '/']
    delimitadoresPular = [' ', '\n', '\t']
    delimitadorQuePodeTerIrmao = ['>', '<', ':']

    nrLinha = 1

    esperaIrmao = False
    esperaFechamentoString = False
    esperaFechamentoLiteral = False

    for i in range(0,len(palavra)):
        if(palavra[i] == '\n'):
            nrLinha += 1
        if (esperaFechamentoLiteral or esperaFechamentoString) and palavra[i] not in ["'", '"']:
            lexema = lexema + palavra[i]
        elif palavra[i] in delimitadores and esperaIrmao:
            lexema = lexema + palavra[i]
            esperaIrmao = False
        elif palavra[i] in delimitadores:
            lexema = palavra[i]
        elif palavra[i] == '.':
            if lexema.isdigit() and len(palavra)>i+1 and palavra[i+1].isdigit() and not esperaFechamentoString and not esperaFechamentoLiteral:
                lexema = lexema + palavra[i]
            else:
                lexema = palavra[i]
        elif palavra[i] in delimitadoresPular:
            lexema = ""
            continue
        else:
            lexema = lexema + palavra[i]
    
        if lexema == '"':
            if esperaFechamentoString:
                token = enumToken.getVString()
                tokens.append(token[0])
                lexemas.append({"lexema": token[1], "linha": nrLinha})
            esperaFechamentoString = not esperaFechamentoString
        elif esperaFechamentoString:
            continue
        if(lexema == "'"):
            if esperaFechamentoLiteral:
                token = enumToken.getLiteral()
                tokens.append(token[0])
                lexemas.append({"lexema": token[1], "linha": nrLinha})
            esperaFechamentoLiteral = not esperaFechamentoLiteral
        elif esperaFechamentoLiteral:
            continue
        if len(palavra)>i+1 and palavra[i] in delimitadorQuePodeTerIrmao and enumToken.getByLexeme(lexema + palavra[i+1]) is not None:
            esperaIrmao = True
            continue
        if enumToken.getByLexeme(lexema) is not None:
            token = enumToken.getByLexeme(lexema)
            tokens.append(token.code)
            lexemas.append({"lexema": token.lexeme, "linha": nrLinha})
            lexema = ""
        elif (len(palavra)>i+1 and (palavra[i+1] in delimitadores or palavra[i+1] in delimitadoresPular or palavra[i+1] =='.')) or len(palavra)==i+1:
            if(palavra[i+1] == '.' and lexema.isdigit() and len(palavra)>i+2 and palavra[i+2].isdigit()):
                continue
            if lexema.isdigit() :
                token = enumToken.getNInt()
                tokens.append(token[0])
                lexemas.append({"lexema": token[1], "linha": nrLinha})
                lexema = "" 
            elif is_float(lexema):
                token = enumToken.getNReal()
                tokens.append(token[0])
                lexemas.append({"lexema": token[1], "linha": nrLinha})
                lexema = ""
            else:
                token = enumToken.getIdent()
                tokens.append(token[0])
                lexemas.append({"lexema": lexema, "linha": nrLinha})

    print(palavra)
    print("Token: ", tokens)
    print("Lexema: ", lexemas)

    for i in range(0,len(tokens)):
        print("Token: ", tokens[i], " Linha: ", lexemas[i]["linha"], " Lexema: ", lexemas[i]["lexema"])
        print("")
    