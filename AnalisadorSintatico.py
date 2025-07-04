from tokens import Token as enumToken
from TabelaParsing import matriz as TabelaParsing
from Producoes import Producoes
from FirstFollow import matriz as FirstFollow
from AnalisadorSemantico import Semantico

def getFirstFollow(tokens):
    str=''
    for i in range(len(tokens)):
        str += enumToken.getByCode(tokens[i]).lexeme
        if i == len(tokens)-2:
            str += " ou "
        elif i != len(tokens)-1:
            str += " "
    return str

semantico = Semantico()

def executarAcaoSemantica(tokenAtual, tokens, indexAtual):
    if tokenAtual == 22:  # begin
        semantico.nivel += 1
    if tokenAtual == 18:  # end
        semantico.removerVariaveisPeloNivel(semantico.nivel)
        semantico.nivel -= 1
    if tokenAtual == 16:  # ident
        semantico.tratarIdentEncontrado(tokens, indexAtual)
    if tokenAtual in (16, 11, 12, 13, 23):
        semantico.validarOperacaoMatematica(tokens, indexAtual)

def analisarSintaxe(tokens):
    
    i = 0
    pilha = [43, 45]
    tokens.append({"token": 43, "linha": 0, "lexema": "$"})
    terminou = False
    while not terminou:
        
        print("")
        print("pilha: ", pilha)
        topo = pilha.pop()
        
        if(i >= len(tokens)):
            print("Erro de sintaxe: Esperado EOF e encontrado ", enumToken.getByCode(topo).lexeme)
            semantico.mostrarErros()
            return False
        if topo<43 or topo > 100:
            print("Terminal encontrado: ", topo)
            print("buscando: ", tokens[i])
            if topo == tokens[i]['token']:
                executarAcaoSemantica(topo, tokens, i)
                i+=1
            else:
                print("Erro de sintaxe na linha "+str(tokens[i]['linha'])+": Esperado " + enumToken.getByCode(topo).lexeme + " e encontrado " +tokens[i]['lexema'] )
                semantico.mostrarErros()
                return False
        elif(topo!=43): # não terminal
            print("Não terminal encontrado: ", topo, " - ", enumToken.getByCode(topo).lexeme)          
            print("buscando: ", tokens[i])
            if TabelaParsing[topo][tokens[i]['token']] != 0:
                conteudo = Producoes.getByCode(TabelaParsing[topo][tokens[i]['token']]).cpd
                
                if conteudo != None:
                    conteudo = conteudo[::-1]
                    for cont in conteudo: 
                        pilha.append(cont)
            else:
                print("Erro de sintaxe na linha " + str(tokens[i]['linha']) + ": Encontrado " + str(tokens[i]['lexema']) + " esperando " + getFirstFollow(FirstFollow[topo]))
                semantico.mostrarErros()
                return False
        else: # topo==43
            if(tokens[i]["token"] == 43):
                print("Análise sintática concluída com sucesso!")
                terminou = True
            else:
                print("Erro de sintaxe na linha " + str(tokens[i]['linha']) + ": Esperado " + enumToken.getByCode(topo).lexeme + " e encontrado " + str(tokens[i]['lexema']) )
                semantico.mostrarErros()
                return False
    semantico.mostrarErros()
    return True
