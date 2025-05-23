from AnalisadorLexico import analisarArquivo
from Producoes import Producoes
from AnalisadorSintatico import analisarSintaxe

#Producoes.escreverGramatica();

tokens = analisarArquivo("exemplos/mainColadinho.txt") # {token, linha, lexema}
analisarSintaxe(tokens)
