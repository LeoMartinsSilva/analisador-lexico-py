from AnalisadorLexico import analisarArquivo
from Producoes import Producoes
from AnalisadorSintatico import analisarSintaxe
from AnalisadorSemantico import analisarSemantica

#Producoes.escreverGramatica();

tokens = analisarArquivo("exemplos/completo.txt") # {token, linha, lexema}
if(analisarSintaxe(tokens)):
    analisarSemantica(tokens)