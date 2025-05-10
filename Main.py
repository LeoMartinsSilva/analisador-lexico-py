from AnalisadorLexico import analisarArquivo
from Producoes import Producoes
from AnalisadorSintatico import analisarSintaxe

#Producoes.escreverGramatica();

#analisarArquivo("exemplos/forEWhile.txt")
tokens = analisarArquivo("exemplos/procedure.txt")
analisarSintaxe(tokens)
#analisarArquivo("exemplos/mainColadinho.txt")
#analisarArquivo("exemplos/string.txt")
