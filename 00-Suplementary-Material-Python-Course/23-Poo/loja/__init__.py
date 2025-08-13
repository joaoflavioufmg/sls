#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Vitrine: Não importamos nem expomos a super-classe 'Pessoa'
# Expomos apenas aquilo que de fato é importante
from .cliente import Cliente
from .vendedor import Vendedor
from .compra import Compra


__all__ = ['Cliente', 'Vendedor', 'Compra']
