from tokens import Token as enumToken
from TabelaParsing import matriz as TabelaParsing
from Producoes import Producoes

def analisarSintaxe(tokens):
    i = 0
    pilha = [43, 45]
    topo = pilha.pop()
    terminou = False
    while not terminou:
        if(i >= len(tokens)):
            print("Erro de sintaxe: Esperado " + str(tokens[i]) + " e encontrado EOF")
            return False
        print("pilha: ", pilha)
        if topo<=43 or topo > 100:
            print("Terminal encontrado: ", topo);
            print("buscando: ", tokens[i]);
            if topo == tokens[i]:
                topo = pilha.pop()
                i+=1
            else:
                print("Erro de sintaxe: Esperado " + str(tokens[i]) + " e encontrado " + str(topo))
                return False
        else: # não terminal
            print("Não terminal encontrado: ", topo)          
            print("buscando: ", tokens[i])
            if TabelaParsing[topo][tokens[i]] != 0:
                conteudo = Producoes.getByCode(TabelaParsing[topo][tokens[i]]).cpd
                
                if conteudo != None:
                    conteudo = conteudo[::-1]
                    for cont in conteudo: 
                        pilha.append(cont)
                topo = pilha.pop()
            else:
                print("Erro de sintaxe: Esperado " + str(tokens[i]) + " e encontrado " + str(topo))
                return False
        if(topo == 43):
            if(tokens[i] == 43):
                print("Análise sintática concluída com sucesso!")
                terminou = True
            else:
                print("Erro de sintaxe: Esperado " + str(topo) + " e encontrado " + str(tokens[i]))
                return False
    return True
