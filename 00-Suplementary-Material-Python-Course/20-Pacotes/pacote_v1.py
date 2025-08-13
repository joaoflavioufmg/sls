#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pacote1 import modulo1

print(type(modulo1))
print(modulo1.soma(2, 3))


from pacote1 import modulo1 as m1
# Agora o nome 'modulo1' não é mais válido. Adota-se 'm1'
print(m1.soma(2, 3))
