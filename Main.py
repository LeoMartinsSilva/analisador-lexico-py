import numpy as np
from tokens import Token as enumToken
palavra = 'program >= end. \';\' \";\"'

print(palavra)

lexema = '';

tokens = []
lexemas = []
delimitadores = ['{', '}', ';', '(', ')', '\'', '\"', ',', ':', '=', '!', '<', '>', '+', '-', '*', '/',  '.']
delimitadoresPular = [' ', '\n', '\t']
delimitadorQuePodeTerIrmao = ['>', '<', ':']

esperaIrmao = False
esperaFechamentoString = False
esperaFechamentoLiteral = False

for i in range(0,len(palavra)):
    if palavra[i] in delimitadores and esperaIrmao:
        lexema = lexema + palavra[i]
        esperaIrmao = False
    elif palavra[i] in delimitadores:
        lexema = palavra[i]
    elif palavra[i] not in delimitadoresPular:
        lexema = lexema + palavra[i]
    else:
        lexema = ""
        continue

    print("Lexema: ", lexema)
    
    if len(palavra)>i+1 and palavra[i] in delimitadorQuePodeTerIrmao and enumToken.getByLexeme(lexema + palavra[i+1]) is not None:
        esperaIrmao = True
        continue
    if lexema in ['\'', '\"']:
        esperaFechamentoString = not esperaFechamentoString
    elif esperaFechamentoString or esperaFechamentoLiteral:
        continue
    if enumToken.getByLexeme(lexema) is not None:
        token = enumToken.getByLexeme(lexema)
        tokens.append(token.code)
        lexemas.append(token.lexeme)
    if lexema in delimitadores:
        lexema = ""

"""for i in range(0,len(tokens)):
    print("Token: ", tokens[i])
    print("Lexema: ", lexemas[i])
    print("")
"""
print("Token: ", tokens)
print("Lexema: ", lexemas)