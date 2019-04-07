#!/usr/bin/env python
# coding: utf-8

# autores: Gabriel de Souza Barreto, Guilherme Bastos de Oliveira
# objetivo: implementar uma classe para manter dados dos outros servidores
# última modificação: 04/06/2018

import time
from utils import *

class Clone:
    def __init__(self, id, id_origem):
        self.id = id
        self.status = 'F'
        self.t_desde_checagem = 0

    # atualiza status caso o parâmetro recebido seja diferente do atual
    def atualizaStatus(self, status):
        self.t_desde_checagem = time.time()
        if self.status != status:
            self.status = status
            safePrint("[M] - status de " + str(self.id) + " atualizado para " + status)

    # verifica se passou tempo limite entre heartbeats recebidos
    def checa(self):
        if time.time() > self.t_desde_checagem + T_PADRAO:
            self.atualizaStatus('F')
