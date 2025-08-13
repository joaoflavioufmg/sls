#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pacote1 import modulo1, modulo2
from pacote2 import modulo1 as m1_sub

# Chamar funções de forma explícita a partir do módulo carregado
print()
print('Soma:', modulo1.soma(2,3))
print('Subtração:', m1_sub.sub(2,3))
print()
modulo2.main()
