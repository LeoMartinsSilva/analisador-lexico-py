from AnalisadorLexico import analisarArquivo
from Producoes import Producoes
from AnalisadorSintatico import analisarSintaxe

#Producoes.escreverGramatica();

tokens = analisarArquivo("exemplos/procedure.txt")
print(tokens)
analisarSintaxe(tokens)
