from tokens import Token as enumToken
import re

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def analisarArquivo(nomeArquivo):
    with open(nomeArquivo, 'r', encoding="UTF-8") as arquivo:
        conteudo = arquivo.read()
        return analisarPalavra(conteudo)

def temAcentosOuCaracteresEspeciais(s):
    return bool(re.search(r'[^a-zA-Z0-9\s]', s))


def analisarPalavra(palavra):
    lexema = '';
    tokens = []
    lexemas = []
    erros = []

    delimitadores = ['{', '}', ';', '(', ')', '\'', '\"', ',', ':', '=', '!', '<', '>', '+', '-', '*', '/']
    delimitadoresPular = [' ', '\n', '\t']
    delimitadorQuePodeTerIrmao = ['>', '<', ':']

    nrLinha = 1

    esperaIrmao = False
    esperaFechamentoString = False
    esperaFechamentoLiteral = False
    comentandoLinha = False
    comentandoBloco = False
    podeIdent = True

    for i in range(0,len(palavra)):
        if(palavra[i] == '\n'):
            nrLinha += 1
            podeIdent = True
            comentandoLinha = False
        if comentandoLinha:
            continue;
        if comentandoBloco:
            if palavra[i] == '/' and len(palavra)>i and palavra[i-1] == '@':
                comentandoBloco = False
                continue
            else:
                continue
        if (esperaFechamentoLiteral or esperaFechamentoString) and palavra[i] not in ["'", '"']:
            lexema = lexema + palavra[i]
        if palavra[i] == "@":
            comentandoLinha = True
            continue
        if palavra[i] == "/" and len(palavra)>i and palavra[i+1] == "@":
            comentandoBloco = True
            continue
        elif palavra[i] in delimitadores and esperaIrmao:
            lexema = lexema + palavra[i]
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
    
        if lexema == '"' and not esperaFechamentoLiteral:
            if esperaFechamentoString:
                token = enumToken.getVString()
                tokens.append(token[0])
                lexemas.append({"lexema": token[1], "linha": nrLinha})
            esperaFechamentoString = not esperaFechamentoString
            continue
        elif esperaFechamentoString:
            continue
        if(lexema == "'") and not esperaFechamentoString:
            if esperaFechamentoLiteral:
                token = enumToken.getLiteral()
                tokens.append(token[0])
                lexemas.append({"lexema": token[1], "linha": nrLinha})
            esperaFechamentoLiteral = not esperaFechamentoLiteral
            continue
        elif esperaFechamentoLiteral:
            continue
        if len(palavra)>i+1 and palavra[i] in delimitadorQuePodeTerIrmao and enumToken.getByLexeme(lexema + palavra[i+1]) is not None:
            esperaIrmao = True
            continue
        
        if enumToken.getByLexeme(lexema) is not None and (palavra[i+1].isdigit() or palavra[i+1].isalpha()) and lexema not in delimitadores and not esperaIrmao:
            continue
        if enumToken.getByLexeme(lexema) is not None:
            esperaIrmao = False
            token = enumToken.getByLexeme(lexema)
            tokens.append(token.code)
            lexemas.append({"lexema": token.lexeme, "linha": nrLinha})
            lexema = ""
        elif (len(palavra)>i+1 and (palavra[i+1] in delimitadores or palavra[i+1] in delimitadoresPular or palavra[i+1] =='.')) or len(palavra)==i+1:
            if(len(palavra)>i+1 and palavra[i+1] == '.' and lexema.isdigit() and len(palavra)>i+2 and palavra[i+2].isdigit()):
                continue
            if lexema.isdigit() :
                token = enumToken.getNInt()
                tokens.append(token[0])
                lexemas.append({"lexema": token[1], "linha": nrLinha})
                if(len(lexema)>4):
                    erros.append({"linha": nrLinha, "lexema": lexema, "erro": "Número maior que 9999"})
                lexema = "" 
            elif is_float(lexema):
                token = enumToken.getNReal()
                tokens.append(token[0])
                lexemas.append({"lexema": token[1], "linha": nrLinha})
                parteInteira, parteDecimal = lexema.split('.')
                if(len(parteInteira)>4):
                    erros.append({"linha": nrLinha, "lexema": lexema, "erro": "Número maior que 9999"})
                if(len(parteDecimal)>2):
                    erros.append({"linha": nrLinha, "lexema": lexema, "erro": "Parte decimal do numero maior que 2 digitos"})
                lexema = ""
            else:
                token = enumToken.getIdent()
                tokens.append(token[0])
                lexemas.append({"lexema": lexema, "linha": nrLinha})
                
                if len(lexema)>64:
                    erros.append({"linha": nrLinha, "lexema": lexema, "erro": "Identificador maior que 64 caracteres"})
                if lexema[0].isdigit():
                    erros.append({"linha": nrLinha, "lexema": lexema, "erro": "Identificador começa com número"})
                if temAcentosOuCaracteresEspeciais(lexema):
                    erros.append({"linha": nrLinha, "lexema": lexema, "erro": "Identificador contém acentos ou caracteres especiais"})

                if not podeIdent and tokens[len(tokens)-2] == token[0]:
                    erros.append({"linha": nrLinha, "lexema": lexemas[len(tokens)-2]["lexema"] + " " + lexema, "erro": "Identificador não pode ter espaço entre letras"})
                podeIdent = False
                
    if(esperaFechamentoLiteral):
        erros.append({"linha": lexemas[len(lexemas)-1]['linha'], "lexema": "'", "erro": "Literal não fechado"})
    if(esperaFechamentoString):
        erros.append({"linha": lexemas[len(lexemas)-1]['linha'], "lexema": '"', "erro": "String não fechada"})

    for i in range(0,len(tokens)):
        print("Token: ", tokens[i], " Linha: ", lexemas[i]["linha"], " Lexema: ", lexemas[i]["lexema"])
        print("")
    
    for i in range(0,len(erros)):
        print("Erro: ", erros[i]["erro"], " Linha: ", erros[i]["linha"], " Lexema: ", erros[i]["lexema"])
        print("")
        
    retorno = [];
    
    for i in range(0,len(tokens)):
        retorno.append({"token": tokens[i], "linha": lexemas[i]["linha"], "lexema": lexemas[i]["lexema"]})
        
    return retorno;