#!/usr/bin/env python
# coding: utf-8

# autores: Gabriel de Souza Barreto, Guilherme Bastos de Oliveira
# objetivo: imprimir log sem interferência entre threads
# última modificação: 04/06/2018

from threading import Lock
import time, datetime

# variável global
print_lock = Lock()

def safePrint(str):
    # adquire trava, imprime com timestamp e libera trava
    global print_lock
    date = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    print_lock.acquire()
    print date, str
    print_lock.release()
