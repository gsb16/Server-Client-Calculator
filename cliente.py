#!/usr/bin/env python
# coding: utf-8

# autores: Gabriel de Souza Barreto, Guilherme Bastos de Oliveira
# objetivo: receber expressões do usuário, fazer requisição e mostrar resultado
# última modificação: 04/06/2018

from utils import *
import sys, socket, struct

if __name__ == "__main__":
    # processamento dos argumentos
    try:
        end_ip = sys.argv[1]
        porta = int(sys.argv[2])
    except:
        print 'Erro dados entrados - uso correto: %s <endereço> <porta> "<expressão>"' % sys.argv[0]
        sys.exit(1)

    descritor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    descritor_socket.settimeout(2)


    try:
        # loop principal
        while 1:
            # lê expressão do usuário
            expressao = raw_input("Entre uma expressão: ")
            dados = struct.pack('ci{}s'.format(len(expressao)), 'R', len(expressao), expressao)

            recebido = False
            # envia requisição até receber resposta
            while not recebido:
                descritor_socket.sendto(dados, (end_ip, porta))
                safePrint("Enviando requisição")
                try:
                    # recebe resposta e mostra resultado ao usuário
                    dados, end = descritor_socket.recvfrom(1024)
                    recebido = True
                    if dados[0] == 'A':
                        tipo, status, valor = struct.unpack('ccf', dados)
                        if status == 'S':
                            safePrint("Resposta recebida: " + str(valor))
                        # descreve o erro para o usuário
                        elif status == ERRO_LETRA:
                            safePrint("ERRO: Expressão contém símbolo inválido (letras)")
                        elif status == ERRO_DIVZERO:
                            safePrint("ERRO: Não é possível realizar divisão por zero")
                        elif status == ERRO_SINTAXE:
                            safePrint("ERRO: Expressão possui erro de sintaxe")
                        elif status == ERRO_DESCONHECIDO:
                            safePrint("ERRO: Ocorreu algum erro ao calcular a expressão")
                except socket.timeout:
                    safePrint("Timeout - não recebi resposta")
    except:
        print "Encerrando execução"
