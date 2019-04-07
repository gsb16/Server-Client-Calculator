#!/usr/bin/env python
# coding: utf-8

# autores: Gabriel de Souza Barreto, Guilherme Bastos de Oliveira
# objetivo: executar instância de servidor
# última modificação: 04/06/2018

import sys
from utils import *
from threading import Thread

if __name__ == "__main__":
    # processamento dos argumentos
    try:
        para_threads = False
        id = int(sys.argv[1])
        end_ip = sys.argv[2]
        porta = int(sys.argv[3])
        print 'Servidor #%d escutando no endereço %s:%d' % (id, end_ip, porta)
    except:
        print "Erro dados entrados - uso correto: <id> <endereço> <porta>"
        exit(-1)

    # setup do singleton servidor e da thread de verificação/envio de status
    servidor = Servidor(id, end_ip, porta)
    thread_status = Thread(target=servidor.statusContinuo, args=[lambda: para_threads])
    thread_status.start()

    try:
        # loop principal
        while 1:
            # recebe e processa mensagem
            dados, end_cliente = servidor.socket_escuta.recvfrom(1024)
            if dados[0] == 'S':
                servidor.processaStatus(dados)
            if dados[0] == 'I':
                servidor.processaInicial(dados)
            if dados[0] == 'R':
                servidor.processaRequisicao(end_cliente, dados)
    # ao receber '^C' encerra execução
    except KeyboardInterrupt:
        safePrint("Encerrado execução")
        # comunica status inativo para outros servidores
        servidor.enviaStatus("F")
        para_threads = True
        thread_status.join()
        exit(-1)
