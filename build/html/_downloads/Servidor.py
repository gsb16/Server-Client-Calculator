#!/usr/bin/env python
# coding: utf-8

# autores: Gabriel de Souza Barreto, Guilherme Bastos de Oliveira
# objetivo: implementar singleton para realizar tarefas do servidor
# última modificação: 04/06/2018

from utils import *
import socket, struct, time

class Servidor:
    def __init__(self, id, end_ip, porta):
        self.id = id
        self.end_ip = end_ip
        self.porta = porta
        self.clones = []
        self.socket_escuta = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.criaListaServidores()
        self.configuraSocket()

    # configuração do socket para escutar multicast e do socket para enviar mensagem
    def configuraSocket(self):
        self.socket_escuta.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_escuta.bind(('', self.porta))
        mreq = struct.pack('4sl', socket.inet_aton(self.end_ip), socket.INADDR_ANY)
        self.socket_escuta.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.socket_envia = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # função alvo da thread de verificação
    def statusContinuo(self, paraThread):
        segundos_passados = time.time()
        self.enviaInicial()
        while not paraThread():
            for serv in self.clones:
                serv.checa()
            if time.time() > segundos_passados + T_HEARTBEAT:
                self.enviaStatus('O')
                segundos_passados = time.time()

    # cria lista (tabela) de clones
    def criaListaServidores(self):
        for i in range(N):
            if i != self.id:
                self.clones.append(Clone(i, self.id))

    # define se é líder
    def lider(self):
        for servidor in self.clones[:self.id]:
            if servidor.status == 'O':
                safePrint("[R] - não sou o líder")
                return False
        safePrint("[R] - sou o líder")
        return True

    # métodos de processamento de mensagens
    def processaStatus(self, dados):
        tipo, origem, valor = struct.unpack('cic', dados)
        if origem != self.id:
            safePrint("[S] - recebi status " + str(valor) + " de " + str(origem))
            offset = 0 if origem < self.id else 1
            self.clones[origem-offset].atualizaStatus(valor)

    def processaInicial(self, dados):
        tipo, origem = struct.unpack('ci', dados)
        if origem != self.id:
            safePrint("[I] - recebi I de " + str(origem))
            offset = 0 if origem < self.id else 1
            self.clones[origem-offset].atualizaStatus('O')
            self.enviaStatus('O')

    def processaRequisicao(self, end_cliente, dados):
        safePrint("[R] - recebi requisição de " + end_cliente[0])
        if self.lider():
            tipo, tam = struct.unpack('ci', dados[:8])
            expressao = struct.unpack('{}s'.format(tam), dados[8:])[0]
            # evita processamento de expressões com letras
            if not any(c.isalpha() for c in expressao): 
                try:
                    self.enviaResposta(end_cliente, eval(expressao))
                # tratamento dos erros
                except ZeroDivisionError:
                    self.enviaRespostaErro(end_cliente, ERRO_DIVZERO)
                except SyntaxError:
                    self.enviaRespostaErro(end_cliente, ERRO_SINTAXE)
                except:
                    self.enviaRespostaErro(end_cliente, ERRO_DESCONHECIDO)
            else:
                self.enviaRespostaErro(end_cliente, ERRO_LETRA)

    # métodos para o envio de mensagens
    def enviaInicial(self):
        safePrint("[I] - enviando I")
        dados = struct.pack('ci', "I", self.id)
        self.socket_envia.sendto(dados, (self.end_ip, self.porta))

    def enviaStatus(self, status):
        safePrint("[S] - enviando status " + status)
        dados = struct.pack('cic', "S", self.id, status)
        self.socket_envia.sendto(dados, (self.end_ip, self.porta))

    def enviaResposta(self, end_cliente, resposta):
        dados = struct.pack('ccf', 'A', SUCESSO, resposta)
        self.socket_envia.sendto(dados, end_cliente)
        safePrint("[A] - respondendo requisição de " + end_cliente[0])

    def enviaRespostaErro(self, end_cliente, erro):
        safePrint("[A] - respondendo requisição de " + end_cliente[0])
        dados = struct.pack('ccf', 'A', erro, 0)
        self.socket_envia.sendto(dados, end_cliente)
