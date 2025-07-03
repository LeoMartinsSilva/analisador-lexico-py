tabela = []
erros = []

def buscarVars(tokens, indexPrimeiraVariavel):
    variaveis = []
    for i in range(indexPrimeiraVariavel, len(tokens)):
        if tokens[i]['token'] == 16:  # Variável
            variaveis.append({"nome": tokens[i]['lexema'], "linha": tokens[i]['linha']})
        elif tokens[i]['token'] == 14 or tokens[i]['token'] == 6 or tokens[i]['token'] == 5:  # Tipo de variável (inteiro, real ou string)
            while len(variaveis) > 0:
                variavel = variaveis.pop(0)
                adicionarIdent(variavel['nome'], tokens[i]['lexema'], 'var', 0, variavel['linha'])
        elif tokens[i]['token'] == 9 or tokens[i]['token'] == 22:  # Fim da declaração de variáveis (se for procedure ou begin)
            break
        
def buscarParametros(tokens, indexPrimeiraVariavel):
    parametros = []
    for i in range(indexPrimeiraVariavel, len(tokens)):
        if tokens[i]['token'] == 16:  # Variável
            parametros.append({"nome": tokens[i]['lexema'], "linha": tokens[i]['linha']})
        elif tokens[i]['token'] == 14 or tokens[i]['token'] == 6 or tokens[i]['token'] == 5:  # Tipo de variável (inteiro, real ou string)
            while len(parametros) > 0:
                parametro = parametros.pop(0)
                adicionarIdent(parametro['nome'], tokens[i]['lexema'], 'param', 1, parametro['linha'])
        elif tokens[i]['token'] == 39:  # Fim da declaração de parâmetros
            break

def adicionarIdent(nome, tipo, categoria, nivel, linha):
    ident = {"nome": nome, "tipo": tipo, "categoria": categoria, "nivel": nivel}
    for item in tabela:
        if item["nome"] == nome:
            erro = {"erro": "Identificador '" + nome + "' duplicado", "linha": linha}
            erros.append(erro)
            return
    tabela.append(ident)

def validarDeclaracao(tokens, index):
    variavel = tokens[index]['lexema']
    encontrou = False
    for item in tabela:
        if item['nome'] == variavel:
            encontrou = True
            break
    if not encontrou:
        erro = {"erro": "Variável '" + variavel +"' não declarada", "linha": tokens[index]['linha']}
        erros.append(erro)
        return False
    return True

def validarAtribuicao(tokens, index):
    variavel = tokens[index]['lexema']
    tipoVariavel = None
    categoria = None
    for item in tabela:
        if item['nome'] == variavel:
            tipoVariavel = item['tipo']
            categoria = item['categoria']
            break
    
    if categoria == "const":
        erro = {"erro": f"Não é possível alterar uma constante", "linha": tokens[index]['linha']}
        erros.append(erro)
        return
    if categoria == "procedure":
        erro = {"erro": f"Não é possível atribuir valor a uma procedure", "linha": tokens[index]['linha']}
        erros.append(erro)
        return
    if categoria == "program":
        erro = {"erro": f"Não é possível atribuir valor a um programa", "linha": tokens[index]['linha']}
        erros.append(erro)
        return
    
    tiposAtribuidos = []
    for i in range(index+2, len(tokens)):
        if tokens[i]['token'] == 31:
            break
        if tokens[i]['token'] == 3:
            break
        if tokens[i]['token'] == 11:
            tiposAtribuidos.append("real")
        if tokens[i]['token'] == 12:
            tiposAtribuidos.append("integer")
        if tokens[i]['token'] == 13:
            tiposAtribuidos.append("literal")
        if tokens[i]['token'] == 23:
            tiposAtribuidos.append("string")
        if tokens[i]['token'] == 16:
            tipoAtribuicao = None
            for item in tabela:
                if item['nome'] == tokens[i]['lexema']:
                    tipoAtribuicao = item['tipo']
                    break
            if tipoAtribuicao:
                tiposAtribuidos.append(tipoAtribuicao)
    for tipoAtribuicao in tiposAtribuidos:
        if tipoVariavel != tipoAtribuicao:
            erro = {"erro": f"Tipo de atribuição inválido para '{variavel}'. Esperado {tipoVariavel}, encontrado {tipoAtribuicao}", "linha": tokens[index]['linha']}
            erros.append(erro)
            return

def validarOperacaoMatematica(tokens, index):    
    tiposOperacao = []
    for i in range(index, len(tokens)):
        if tokens[i]['token'] == 31:
            break
        if tokens[i]['token'] == 23:
            tiposOperacao.append('string')
        if tokens[i]['token'] == 11:
            tiposOperacao.append('real')
        if tokens[i]['token'] == 12:
            tiposOperacao.append('integer')
        if tokens[i]['token'] == 13:
            tiposOperacao.append('literal')
        if tokens[i]['token'] == 16:
            tipoOperacao = None
            for item in tabela:
                if item['nome'] == tokens[i]['lexema']:
                    tipoOperacao = item['tipo']
                    categoria = item['categoria']
                    if categoria == "procedure":
                        erro = {"erro": f"Não é possível realizar operações com uma procedure", "linha": tokens[index]['linha']}
                        erros.append(erro)
                    if categoria == "program":
                        erro = {"erro": f"Não é possível realizar operações com um programa", "linha": tokens[index]['linha']}
                        erros.append(erro)
                    break
            if tipoOperacao:
                tiposOperacao.append(tipoOperacao)
    
    if len(tiposOperacao) > 0:
        tipo = tiposOperacao[0]
        for tipoOp in tiposOperacao:
            if tipoOp != tipo:
                erro = {"erro": f"Tipos incompatíveis na operação matemática. Esperado {tipo}, encontrado {tipoOp}", "linha": tokens[index]['linha']}
                erros.append(erro)
                return
        

def removerVariaveisPeloNivel(nivel):
    for i in range(len(tabela)):
        if tabela[i]['nivel'] == nivel:
            tabela.pop(i)
            break

            
def analisarSemantica(tokens):
    nivel = 0
    for i in range(0,len(tokens)):
        if tokens[i]['token'] == 22:  # begin
            nivel += 1
            continue
        if tokens[i]['token'] == 18:  # end
            removerVariaveisPeloNivel(nivel)
            nivel -= 1
            continue
        if tokens[i]['token'] == 16:
            if tokens[i-1]['token'] == 8:# program
                adicionarIdent(tokens[i]['lexema'], '','program', 0, tokens[i]['linha'])
                continue
            if tokens[i-1]['token'] == 2: #variavel
                buscarVars(tokens, i)
                continue
            if tokens[i-1]['token'] == 9: #procedure
                adicionarIdent(tokens[i]['lexema'], '','procedure', 0, tokens[i]['linha'])
                continue
            if tokens[i-1]['token'] == 21: #const
                adicionarIdent(tokens[i]['lexema'], 'integer','const', 0, tokens[i]['linha'])
                continue
            if tokens[i-3]['token'] == 9 and tokens[i-2]['token'] == 16 and tokens[i-1]['token'] == 39: # reconhecimento de variaveis de procedures 
                buscarParametros(tokens, i)
                continue
            
            
            validarDeclaracao(tokens, i)
            if tokens[i+1]['token'] == 32: # atribuição :=
                validarAtribuicao(tokens, i)
        
        if tokens[i]['token'] in (16, 11, 12, 13, 23): # Ident, real, inteiro, literal ou string
            if tokens[i+1]['token'] in [30, 42, 37, 34]: # + - * /
                validarOperacaoMatematica(tokens, i)
                     

    print(tabela)
    for erro in erros:
        print(f"Erro: {erro['erro']} na linha {erro['linha']}")
    