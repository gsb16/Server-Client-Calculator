#!/usr/bin/env python
# coding: utf-8

# autores: Gabriel de Souza Barreto, Guilherme Bastos de Oliveira
# objetivo: definir constantes e facilitar a importação de códigos auxiliares
# última modificação: 04/06/2018

# constantes

# tempo de intervalo entre heartbeats
T_HEARTBEAT = 8

# tempo de timeout para receber uma resposta
T_TIMEOUT = 2

# tempo máximo entre heartbeats dos clones ativos
T_PADRAO = T_HEARTBEAT + T_TIMEOUT

# número máximo de servidores
N = 3

# tipos de resultados
SUCESSO = 'S'
ERRO_LETRA = 'L'
ERRO_SINTAXE = 'X'
ERRO_DIVZERO = 'Z'
ERRO_DESCONHECIDO = 'D'

# submodulos
from safePrint import *
from Clone import *
from Servidor import *
