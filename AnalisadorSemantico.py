
class Semantico:
    def __init__(self):
        self.tabela = []
        self.erros = []
        self.nivel = 0
        
    def adicionarErro(self, erro):
        print(f"Erro: {erro['erro']} na linha {erro['linha']}")
        self.erros.append(erro)
        
    def mostrarErros(self):
        print("\nErros semânticos:")
        for erro in self.erros:
            print(f"Erro: {erro['erro']} na linha {erro['linha']}")

    def buscarVars(self, tokens, indexPrimeiraVariavel):
        variaveis = []
        for i in range(indexPrimeiraVariavel, len(tokens)):
            if tokens[i]['token'] == 16:  # Variável
                variaveis.append({"nome": tokens[i]['lexema'], "linha": tokens[i]['linha']})
            elif tokens[i]['token'] == 14 or tokens[i]['token'] == 6 or tokens[i]['token'] == 5:  # Tipo de variável (inteiro, real ou string)
                while len(variaveis) > 0:
                    variavel = variaveis.pop(0)
                    self.adicionarIdent(variavel['nome'], tokens[i]['lexema'], 'var', 0, variavel['linha'])
            elif tokens[i]['token'] == 9 or tokens[i]['token'] == 22:  # Fim da declaração de variáveis (se for procedure ou begin)
                break
            
    def buscarParametros(self, tokens, indexPrimeiraVariavel):
        parametros = []
        for i in range(indexPrimeiraVariavel, len(tokens)):
            if tokens[i]['token'] == 16:  # Variável
                parametros.append({"nome": tokens[i]['lexema'], "linha": tokens[i]['linha']})
            elif tokens[i]['token'] == 14 or tokens[i]['token'] == 6 or tokens[i]['token'] == 5:  # Tipo de variável (inteiro, real ou string)
                while len(parametros) > 0:
                    parametro = parametros.pop(0)
                    self.adicionarIdent(parametro['nome'], tokens[i]['lexema'], 'param', 1, parametro['linha'])
            elif tokens[i]['token'] == 39:  # Fim da declaração de parâmetros
                break

    def adicionarIdent(self, nome, tipo, categoria, nivel, linha):
        ident = {"nome": nome, "tipo": tipo, "categoria": categoria, "nivel": nivel}
        for item in self.tabela:
            if item["nome"] == nome:
                erro = {"erro": "Identificador '" + nome + "' duplicado", "linha": linha}
                self.adicionarErro(erro)
                return
        self.tabela.append(ident)
        self.escreverTabela();
        
    def escreverTabela(self):
        
        print("\nTabela alterada:")
        for item in self.tabela:
            print(f"Nome: {item['nome']}, Tipo: {item['tipo']}, Categoria: {item['categoria']}, Nível: {item['nivel']}")

    def validarDeclaracao(self, tokens, index):
        variavel = tokens[index]['lexema']
        encontrou = False
        for item in self.tabela:
            if item['nome'] == variavel:
                encontrou = True
                break
        if not encontrou:
            erro = {"erro": "Variável '" + variavel +"' não declarada", "linha": tokens[index]['linha']}
            self.adicionarErro(erro)
            return False
        return True

    def validarAtribuicao(self, tokens, index):
        variavel = tokens[index]['lexema']
        tipoVariavel = None
        categoria = None
        for item in self.tabela:
            if item['nome'] == variavel:
                tipoVariavel = item['tipo']
                categoria = item['categoria']
                break
        
        if categoria == "const":
            erro = {"erro": f"Não é possível alterar uma constante", "linha": tokens[index]['linha']}
            self.adicionarErro(erro)
            return
        if categoria == "procedure":
            erro = {"erro": f"Não é possível atribuir valor a uma procedure", "linha": tokens[index]['linha']}
            self.adicionarErro(erro)
            return
        if categoria == "program":
            erro = {"erro": f"Não é possível atribuir valor a um programa", "linha": tokens[index]['linha']}
            self.adicionarErro(erro)
            return
        
        tiposAtribuidos = []
        for i in range(index+2, len(tokens)):
            if tokens[i]['token'] == 31:
                break
            if tokens[i]['token'] == 3:
                break
            if tokens[i]['token'] not in [11, 12, 13, 16, 23, 30, 42, 37, 34]: # não é um elemento valido para calculos
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
                for item in self.tabela:
                    if item['nome'] == tokens[i]['lexema']:
                        tipoAtribuicao = item['tipo']
                        break
                if tipoAtribuicao:
                    tiposAtribuidos.append(tipoAtribuicao)
        for tipoAtribuicao in tiposAtribuidos:
            if tipoVariavel != tipoAtribuicao:
                erro = {"erro": f"Tipo de atribuição inválido para '{variavel}'. Esperado {tipoVariavel}, encontrado {tipoAtribuicao}", "linha": tokens[index]['linha']}
                self.adicionarErro(erro)
                return

    def validarOperacaoMatematica(self, tokens, index):
        if tokens[index+1]['token'] not in [30, 42, 37, 34]: # + - * /  
            return
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
                for item in self.tabela:
                    if item['nome'] == tokens[i]['lexema']:
                        tipoOperacao = item['tipo']
                        categoria = item['categoria']
                        if categoria == "procedure":
                            erro = {"erro": f"Não é possível realizar operações com uma procedure", "linha": tokens[index]['linha']}
                            self.adicionarErro(erro)
                        if categoria == "program":
                            erro = {"erro": f"Não é possível realizar operações com um programa", "linha": tokens[index]['linha']}
                            self.adicionarErro(erro)
                        break
                if tipoOperacao:
                    tiposOperacao.append(tipoOperacao)
        
        if len(tiposOperacao) > 0:
            tipo = tiposOperacao[0]
            for tipoOp in tiposOperacao:
                if tipoOp != tipo:
                    erro = {"erro": f"Tipos incompatíveis na operação matemática. Esperado {tipo}, encontrado {tipoOp}", "linha": tokens[index]['linha']}
                    self.adicionarErro(erro)
                    return
    
    def removerVariaveisPeloNivel(self, nivel):
        for i in range(len(self.tabela)):
            if self.tabela[i]['nivel'] == nivel:
                self.tabela.pop(i)
                break
        self.escreverTabela()
    
    def tratarIdentEncontrado(self, tokens, index):
        if tokens[index-1]['token'] == 8:# program
            self.adicionarIdent(tokens[index]['lexema'], '','program', 0, tokens[index]['linha'])
        if tokens[index-1]['token'] == 2: #variavel
            self.buscarVars(tokens, index)
        if tokens[index-1]['token'] == 9: #procedure
            self.adicionarIdent(tokens[index]['lexema'], '','procedure', 0, tokens[index]['linha'])
        if tokens[index-1]['token'] == 21: #const
            self.adicionarIdent(tokens[index]['lexema'], 'integer','const', 0, tokens[index]['linha'])
        if tokens[index-3]['token'] == 9 and tokens[index-2]['token'] == 16 and tokens[index-1]['token'] == 39: # reconhecimento de variaveis de procedures 
            self.buscarParametros(tokens, index)
            
        self.validarDeclaracao(tokens, index)
        if tokens[index+1]['token'] == 32: # atribuição :=
            self.validarAtribuicao(tokens, index)
                        
        
    