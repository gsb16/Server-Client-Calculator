# Trabalho de Redes 2 - 2018/1
## Servidor de alta disponibilidade por replicação

## Autores
### Gabriel de Souza Barreto
### Guilherme Bastos de Oliveira

## Projeto
O objetivo deste trabalho é implementar através de replicação um serviço de calculadora de alta disponibilidade.

A linguagem para desenvolvimento escolhida foi Python por dois motivos, a indicação do professor e a familiaridade com a linguagem dos integrantes do grupo.

O funcionamento do sistema é baseado em vários servidores que, executando o mesmo processo escutam em um grupo multicast, ao receberem uma requisição é decidido (por método que será explicado posteriormente) qual servidor deverá responder a requisição, e então este e apenas este servidor irá responder ao cliente.

## Execução
Para executar o programa cliente:

    python cliente.py <endereço> <porta>


Para executar o programa servidor:

    python servidor.py <id> <endereço> <porta>
