# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_operators.php
# https://www.tutorialspoint.com/python/
# http://python.nilo.pro.br/
#
# Operadores aritmeticos:       + - * / % ** //
# Operadores de comparacao:     == !=  >  < >= <=
# Operadores de atribuicao:     = += -= *= /= %= **= //=
# Operadores por bite: & | ^ ~ << >>
# Operadores logicos: "and", "or", "not"
# Operadores de membros: "in", "not in"
#
import sys
print (sys.version)
# sys.path.append('./ex/')
# ******************************************************************
# Operadores aritmeticos do Python: + - * / % ** //
# ******************************************************************
print('\nOperadores Aritmeticos:')

a = 20
b = 10
c = 0

c = a + b
print('[1]: c =',c)

c = a - b
print('[2]: c =',c)

c = a * b
print('[3]: c =',c)

c = a / b
print('[4]: c =',c)

c = a % b   # Resto da divisao (modulo da divisao)
print('[5]: c =',c)

a = 2
b = 3
c = a**b    # Exponencial: a "elevado a" b
print('[6]: c =',c)

a = 10
b = 6
c = a//b    # Parte inteira de uma divisao: 10//9 = 1
print('[7]: c =',c)
print()
# ******************************************************************
# Operadores de comparacao: # == !=  >  < >= <=
# ******************************************************************
print('\nOperadores de comparacao:')

a = 21
b = 10
c = 0

if (a == b):
    print('[1]: "a" eh igual a "b"')
else:
    print('[1]: "a" nao eh igual a "b"')

if (a != b):
    print('[2]: "a" nao eh igual a "b"')
else:
    print('[2]: "a" eh igual a "b"')

if (a > b):
    print('[3]: "a" eh maior que "b"')
else:
    print('[3]: "a" nao eh maior que "b"')

if (a < b):
    print('[4]: "a" eh menor que "b"')
else:
    print('[4]: "a" nao eh menor que "b"')

if (a >= b):
    print('[6]: "a" eh maior ou igual a "b"')
else:
    print('[6]: "a" nao eh maior ou igual a "b"')

if (a <= b):
    print('[7]: "a" eh menor ou igual a "b"')
else:
    print('[7]: "a" nao eh menor ou igual a "b"')
print()
# ******************************************************************
# Operadores de atribuicao: = += -= *= /= %= **= //=
# ******************************************************************
print('\nOperatores de atribuicao:')

a = 21
b = 10
c = 0

c = a + b   # c recebe a soma de a e b
print('[1]:', c)

c += a      # a acumula um valor de a: c = c + a
print('[2]:', c)

c *= a      # c = c * a
print('[3]:', c)

c /= a      # c = c / a (float, em funcao da divisao)
print('[4]:', c)

c = 200
c %= a
print('[5]:', c)

c **= a
print('[6]:', c)

c //= a
print('[7]:', c)
print()
# ******************************************************************
# Operadores por bite: & | ^ ~ << >>
# Atencao! Nao confundir com operadores booleanos: && e ||
# ******************************************************************
# Operador: & (e)
    # 0 & 0 == 0
    # 0 & 1 == 0
    # 1 & 0 == 0
    # 1 & 1 == 1

# Operador: | (ou)

    # 0 | 0 == 0
    # 0 | 1 == 1
    # 1 | 0 == 1
    # 1 | 1 == 1

# Operador: ^ (ou exclusivo: XOR)

    # 0 ^ 0 == 0
    # 0 ^ 1 == 1
    # 1 ^ 0 == 1
    # 1 ^ 1 == 0

# Operador: ~ (nao : NOT) Muda o bit para seu oposto
# O maior bit na variavel int eh chamado "sign bit", por isso o negativo.

    # int a = 103;    // binario:  0000000001100111
    # int b = ~a;     // binario:  1111111110011000 = -104
    # ~x = -x-1

# Operador: << ou >> (operador de mudanca esquerdo ou direito: shift operator)
# Muda os bits para esquerda ou direita

    # int a = 5;        // binario: 0000000000000101
    # int b = a << 3;   // binario: 0000000000101000, ou 40
    # int c = b >> 3;   // binario: 0000000000000101, ou de volta a 5

 # Por exemplo, para gerar potencia de 2, use:

    # 1 <<  0  ==    1
    # 1 <<  1  ==    2
    # 1 <<  2  ==    4
    # 1 <<  3  ==    8
    # ...
    # 1 <<  8  ==  256
    # 1 <<  9  ==  512
    # 1 << 10  == 1024

# O tipo int eh um valor 16-bit, entao, ao usar "&" entre dois int causa 16 operacoes AND simultaneamente, exemplo:
#
#     int a =  92;    // em binario: 0000000001011100
#     int b = 101;    // em binario: 0000000001100101
#     int c = a & b;  // resulta:    0000000001000100, ou 68 em decimal.

print('\nOperadores por bite:')

a = 60      # 60 = 0011 1100
b = 13      # 13 = 0000 1101
c = 0

c = a & b   # 12 = 0000 1100
print('[1]:', c)

c = a | b   # 61 = 0011 1101
print('[2]:', c)

c = a ^ b   # 49 = 0011 0001
print('[3]:', c)

c = ~a      # -61 = 1100 0011
print('[4]:', c)

c = a << 2  # 240 = 1111 0000
print('[5]:', c)

c = a >> 2  # 15 = 0000 1111
print('[6]:', c)

print()
# ******************************************************************
# Operadores logicos: "and", "or", "not"
# ******************************************************************

print('\nOperadores logicos:')

a = 10
b = 20
c = 0

# "a" eh diferente de zero e "b" eh diferente de zero, portanto...
if (a and b):
    print('[1]: "a" e "b" sao True')
else:
    print('[1]: Um dos dois: "a" ou "b" nao eh True')

if (a or b):
    print('[2]: Um dos dois: "a" ou "b" eh True ou ambos sao True')
else:
    print('[2]: Nem "a" nem "b" sao True')

# Agora "a" eh zero
a = 0

if (a and b):
    print('[3]: "a" e "b" sao True')
else:
    print('[3]: Um dos dois: "a" ou "b" nao eh True')

if (a or b):
    print('[4]: Um dos dois: "a" ou "b" eh True ou ambos sao True')
else:
    print('[4]: Nem "a" nem "b" sao True')

if not(a and b):
    print('[5]: Nem "a" nem "b" sao True')
else:
    print('[5]: "a" e "b" sao True')

print()
# ******************************************************************
# Operadores de membros: "in", "not in"
# ******************************************************************
print('\nOperadores de membros:')

a = 10
b = 20
lista_01 = [1, 2, 3, 4, 5 ]

if ( a in lista_01 ):
   print("[1] \"a\" esta disponivel na lista_01")
else:
   print("[1] \"a\" nao esta disponivel na lista_01")

if ( b not in lista_01 ):
   print("[2] \"b\" nao esta disponivel na lista_01")
else:
   print("[2] \"b\" esta disponivel na lista_01")

a = 2
if ( a in lista_01 ):
   print("[3] \"a\" esta disponivel na lista_01")
else:
   print("[3] \"a\" nao esta disponivel na lista_01")

print()
# ******************************************************************
# Operacoes basicas
# ******************************************************************
# Subtração
print(5-3)

# Subtração e adicao
print(10-4+2)

# Multiplicação e divisao
print(2*10)

print(20/4)

# Exponenciacao
print(2**3)

# Resto da divisao inteira
print(10 % 3)
print(16 % 7)
print(63 % 8)

# Variaveis
a = 2
b = 3
print (a + b)
# Outra forma...
print (2 + 3)
# Ou..
print (5)
print()
# ******************************************************************
# Relacao de precedencia e operacoes
# ******************************************************************
x = 10 * 3 + 5 - 3
print(x)

x = 10 / 3      # vira float
print(x)

x = 10 // 3     # inteiro da divisao
print(x)

x = 10 % 3      # Resto da divisao
print(x)

x = 10**3       # Potencia: "elevado"
print(x)
print()
# ******************************************************************
# Operadores not, and, or
# ******************************************************************
# not
print(not True)
print(not False)
print()

# and
print(True and True)
print(True and False)
print(False and True)
print(False and False)
print()

# or
print(True or True)
print(True or False)
print(False or True)
print(False or False)
print()

x = (10 or 3)   # Avalia a expressao: Se verdadeiro... imprime o primeiro
print(x)

x = (10 and 3)  # Avalia a expressao: Se verdadeiro... imprime o ultimo
print(x)

for x in range(0,10):   # range vai de 0 ate n-1
    print("%d\t" %x)

print()
# Aqui o valor de x eh 9
print(x < 10)   # Verdadeiro
print(x >= 10)  # Falso
print()

# ******************************************************************
# Exemplos: Calculo de aumento do salario e de divida
# ******************************************************************
salário = 1500
aumento = 5
print (salário + (salário * aumento / 100))

# Alternativa...
print (1500 + (1500 * 5 / 100))
print()

# Sequencia de valores na mesma variavel
divida = 0
compra = 100
divida = divida + compra
compra = 200
divida = divida + compra
compra = 300
divida = divida + compra
compra = 0
print(divida)
print()

# Impressao de 1 a 3 de formas alternativas
print(1)
print(2)
print(3)
print()

x = 1
print(x)
x = 2
print(x)
x = 3
print(x)
print()

x = 1
print(x)
x = x + 1
print(x)
x = x + 1
print(x)
print()
# ******************************************************************
# Variaveis logicas e operacoes
# ******************************************************************

resultado = True
aprovado = False
print(resultado)
print(aprovado)
print()

a = 1       # a recebe 1
b = 5       # b recebe 5
c = 2       # c recebe 2
d = 1       # d recebe 1
print(a == b)     # a é igual a b ?
print(b > a)       # b é maior que a?
print(a < b)       # a é menor que b?
print(a == d)     # a é igual a d?
print(b >= a)     # b é maior ou igual a a?
print(c <= b)     # c é menor ou igual a b?
print(d != a)     # d é diferente de a?
print(d != b)     # d é diferente de b?
print()

nota = 8
média = 7
aprovado = nota > média
print(aprovado)
print()

# ******************************************************************
# Exercicios
# ******************************************************************
print(50*"-")
print("Exercicios")
print(50*"-")
print(10 + 20 * 30)
print(4 ** 2 / 30)
print((9 ** 4 + 2) * 6 - 1)
print(50*"-")

# efetuando apenas uma operação por linha,
# temos a seguinte ordem de cálculo:
# 0 --> 10 % 3 * 10 ** 2 + 1 - 10 * 4 / 2
# 1 --> 10 % 3 * 100     + 1 - 10 * 4 / 2
# 2 --> 1      * 100     + 1 - 10 * 4 / 2
# 3 -->          100     + 1 - 10 * 4 / 2
# 4 -->          100     + 1 - 40     / 2
# 5 -->          100     + 1 - 20
# 6 -->          101         - 20
# 7 -->                        81

print(10 % 3 * 10 ** 2 + 1 - 10 * 4 / 2)
print(50*"-")

a = 3
b = 5
print(2*a*3*b)
print(50*"-")

a = 2
b = 3
c = 4
print (a + b + c)
print(50*"-")

salário = 750
aumento = 15
print(salário + (salário * aumento / 100))
print(50*"-")

a, b, c, d, e, f = 1, 2, 3, 0, 5, 3

print(a==c) # False (a==c)
print(a<b)  # True  (a<b)
print(d>b)  # False (d>b)
print(c!=f) # False (c!=f)
print(a==b) # False (a==b)
print(c<d)  # False (c<d)
print(b>a)  # True (b>a)
print(c>=f) # True (c>=f)
print(f>=c) # True (f>=c)
print(c<=c) # True (c<=c)
print(c<=f) # True (c<=f)
print(50*"-")

a, b, c = True, False, True

print(a and a)  # True (a and a)
print(b and b)  # False (b and b)
print(not c)    # False (not c)
print(not b)    # True (not b)
print(not a)    # False (not a)
print(a and b)  # False (a and b)
print(b and c)  # False (b and c)
print(a or c)   # True (a or c)
print(b or c)   # True (b or c)
print(a or c)   # True (a or c)
print(b or c)   # True (b or c)
print(c or a)   # True (c or a)
print(c or b)   # True (c or b)
print(c or c)   # True (c or c)
print(b or b)   # False (b or b)
print(50*"-")

materia1 = 8.2
materia2 = 7
materia3 = 7.01

print(materia1 > 7 and materia2 > 7 and materia3 > 7)   # False
print(materia1 >=7 and materia2 >=7 and materia3 >=7)   # True
print(50*"-")
