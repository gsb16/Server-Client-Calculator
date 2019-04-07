Relatório Técnico
=================
O Objetivo do trabalho
~~~~~~~~~~~~~~~~~~~~~~
O objetivo deste trabalho é implementar através de replicação de servidores um serviço de calculadora de alta disponibilidade.

A linguagem para desenvolvimento escolhida foi Python devido a indicação do professor e a familiaridade com a linguagem por parte dos integrantes do grupo.

O funcionamento do sistema é baseado em vários servidores que, executando o mesmo processo, escutam em um grupo multicast. Ao receberem uma requisição é decidido (por método que será explicado posteriormente) qual servidor deverá responder a requisição, e então este e apenas este servidor irá responder ao cliente.

O grupo de servidores
~~~~~~~~~~~~~~~~~~~~~
Cada clone possui um identificador, que é informado no ínicio de sua execução.
Um processo servidor possui três funções básicas:

- avisar periodicamente ao grupo que está ativo (heartbeat)
- determinar situação (ativo/inativo) dos outros servidores
- quando for o servidor líder responder requisições do cliente 

As funções de avisar ao grupo seu status e determinar a situação dos clones é realizada por uma thread filha do processo principal, que por sua vez apenas recebe mensagens e as processa de acordo.

O cliente
~~~~~~~~~
O programa cliente possui um funcionamento bem simples:

1. recebe expressão do usuário
2. faz requisição
3. espera receber resposta por por um tempo T_TIMEOUT
    - recebeu: mostra o resultado recebido
    - não recebeu (timeout): volta ao passo 2
4. volta ao passo 1 até ser encerrado (:kbd:`Ctrl-C`)

Execução
========
Para executar o programa cliente::

    python cliente.py <endereço> <porta>


Para executar o programa servidor::

    python servidor.py <id> <endereço> <porta>

.. caution::
    Como o projeto ocorre sobre comunicação multicast, é necessário utilizar endereços IP reservados para este uso

    Recomenda-se o endereço IPv4 230.0.0.1

Decisões de projeto
===================

Organização do Código
~~~~~~~~~~~~~~~~~~~~~
A organização do código é relativamente simples (veja a :ref:`fontes`):

- arquivo :ref:`cliente` contém o código referente a leitura de expressão do usuário, envio de requisição para os servidores, recebimento do resultado e exibição do valor recebido 
- arquivo :ref:`servidor` contém o código referente a criação da thread responsável por envio de heartbeat e monitoramento do status dos outros servidores. O processo principal recebe, processa e envia mensagens
- arquivos do diretório :ref:`dirutils`:
    - o arquivo :ref:`init` contém um conjunto de constantes e importa os arquivos adicionais encontrados no diretório :file:`utils`
    - o arquivo :ref:`utilsServidor` definição da classe Servidor que contém todos os métodos usados em uma instância servidor 
    - o arquivo :ref:`Clone` definição da classe Clone para monitoramento dos outros servidores 
    - o arquivo :ref:`safePrint` fornece uma função para permitir impressão de log sem interferência entre as threads

Funcionamento da calculadora
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
O programa cliente recebe do usuário uma expressão em formato de string. Essa string é enviada ao serviço de calculadora.
O servidor passa a expressão como parâmetro para a função `eval() <https://docs.python.org/2/library/functions.html#eval>`_, que retorna o valor caso obtenha sucesso, ou levanta uma exceção em casos de erros.
Quando ocorre erro, o servidor envia uma mensagem informando ao cliente.

.. note::
    São executadas apenas expressões matemáticas que não contenham letras para evitar o processamento de instruções maliciosas.

    Se a expressão conter uma comparação, então o resultado será 1.0 caso verdadeira ou 0.0 caso contrário.

Erros
~~~~~
O servidor responde a requisição, em casos de erro, com um dentre quatro tipos: ERRO_SINTAXE, ERRO_LETRA, ERRO_DIVZERO e ERRO_DESCONHECIDO ::

    Entre uma expressão: 8/0
    17:48:08 Enviando requisição
    17:48:08 ERRO: Não é possível realizar divisão por zero
    Entre uma expressão: ataque_hacker()
    17:48:13 Enviando requisição
    17:48:14 ERRO: Expressão contém símbolo inválido (letras)
    Entre uma expressão: 1++
    17:48:17 Enviando requisição
    17:48:17 ERRO: Expressão possui erro de sintaxe
    Entre uma expressão: 2**1024
    17:48:22 Enviando requisição
    17:48:22 ERRO: Ocorreu algum erro ao calcular a expressão


Escolha do líder
~~~~~~~~~~~~~~~~
O líder é o clone de menor identificador que está ativo.

Definindo servidores (in)ativos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Todo servidor, ao ser iniciado, envia um heartbeat inicial e recebe como resposta o heartbeat de todos os outros servidores em execução.
Um servidor constantemente verifica se seus clones estão ativos, ou seja, se tempo transcorrido desde o último heartbeat recebido é menor que o tempo T_PADRAO. Caso contrário, este clone é considerado inativo até o recebimento do próximo heartbeat. Um servidor ao ser encerrado envia uma mensagem de encerramento e é considerado inativo por todos os outros.

Datagramas criados
~~~~~~~~~~~~~~~~~~
Todos os datagramas são iniciados por um byte que armazena um 'char' e informa qual o tipo do datagrama. Foram criados quatro tipos diferentes para o trabalho:

- Tipo 'I': mensagem enviada quando o servidor é iniciado (heartbeat inicial) avisando que está online e pedindo o status dos clones ::

    tipo (char) | origem (int)

- Tipo 'S': mensagem enviada para informar o status, que é um heartbeat periódico, uma mensagem de encerramento ou uma resposta a um heartbeat inicial ::

    tipo (char) | origem (int) | valor (char)

- Tipo 'R': mensagem enviada pelo cliente ao grupo de servidores que contém uma expressão a ser calculada (requisição) ::

    tipo (char) | tam (int) | expressao (string)

- Tipo 'A': mensagem de resposta enviada pelo líder ao cliente contendo o valor da expressão ou o tipo do erro ::

    tipo (char) | sucesso (char) | valor (float)
