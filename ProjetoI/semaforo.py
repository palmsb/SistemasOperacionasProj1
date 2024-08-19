# UFBA - Universidade Federal da Bahia
# Semestre 2024.1
# MATA58 - T02 - Sistemas Operacionais
# Docente: Robespierre Dantas
# Discente: Paloma Brito

# Projeto I - Jogo com Condições de Corrida

# Python: 3.12.5

# INSTRUÇÕES:
# o jogo possui importação do arquivo SemaforoClasse.py, por favor manter na mesma pasta.
# A verão de Python utilizada é a 3.12.5

# Através de uma IDE, acesse a pasta que contém os arquivos no explorar, baixe a extensão Python e clique no botão de 'Run Code';
# No terminal, acesse o local do arquivo onde encontra-se a pasta, por exemplo se os arquivos estiverem na pasta ProjetoI, utilize o comando no terminal (p/ windows): cd C:Users/aluno1/Documents/Semestre2024.1/SO/ProjetoI 
# clique em Enter, em seguida digite python semaforo.py ou python mutex.py e clique em Enter.

# DESCRIÇÃO

# O jogo escolhido para ser abordado nessa temática, foi um jogo simples, básico e conhecido: O Jogo da Memória.
# Ainda por ser conhecido, penso que não seja necessário o alongamento dessa explicação, contudo, o jogo
# tem como objetivo obter pares iguais em um tabuleiro de cartas, organizadas de forma aleatória, escolhendo um par por vez
# com isso, ao achar os pares, o jogador pontua e as cartas são retiradas do tabuleiro, o jogo se encerra quando não houverem mais pares
# e vence o jogador que tenha feito mais pares. Na implementação do código a seguir, pode-se acompanhar que haverão threads
# responsaveis por simular os jogadores que escolhem as cartas do tabuleiro, no código foi implantado mecanismos de controle do acesso
# ao tabuleiro e alternação de turnos para evitar as condições de corrida.


# Qual a condição de corrida?

# Primeiro: Acesso ao tabuleiro, com as operações de leitura do valor, consulta e verificação das cartas são iguais para formarem pares.
# Segundo: temos os turnos, e fazer esse controle é essencial para garantir que somente um jogador faça uma jogada por vez,


# Quais as soluções implementadas?

# Escolhi para esse jogo utilizar Mutex e "Semaforo", porém como não podemos usar bibliotecas prontas, resolvi implementar o semaforo
# não afirmo que é 100%, mas sim uma tentativa de aproximação melhor explicada em video.

import random
import threading
import time
from semaforoClasse import Semaforo  # Importando o semáforo manual

# criando o tabuleiro
tamanhoTabuleiro = 4  # deve ser um número par
tabuleiro = list(range(tamanhoTabuleiro)) * 2
random.shuffle(tabuleiro)

# criando variavéis de controle
pontuacao = [0, 0]
jogadas = 0
maximoJogadas = len(tabuleiro) // 2  #numero maximo de cartas que podem ser encontradas no tabuleiro durante o jogo

# utilização do semáforo "manual" para controle de turno e acesso ao tabuleiro
semaforoTurno = Semaforo(1)  # semáforo para controle de turno 
semaforoTabuleiro = Semaforo(1)  # semáforo controle de acesso ao tabuleiro

# funções para controle de acesso ao turno
def captaTurno(thread_id): 
    semaforoTurno.acquire() 

def liberaTurno(): 
    semaforoTurno.release()

def jogar(thread_id):
    global jogadas, pontuacao
    while jogadas < maximoJogadas:
        captaTurno(thread_id) #turno

        # começar o jogo escolhendo as cartas
        while True:
            semaforoTabuleiro.acquire()  # controle de acesso exclusivo ao tabuleiro por semaforo
            escolha = random.sample(range(len(tabuleiro)), 2)
            if escolha[0] != escolha[1] and tabuleiro[escolha[0]] is not None and tabuleiro[escolha[1]] is not None:
                break
            semaforoTabuleiro.release()  # se a escolha der match a jogada pode ser continuada

        carta1, carta2 = escolha
        print(f"O jogador {thread_id + 1} escolheu as cartas {carta1} e {carta2}.")

        # ao achar, há a verificação dos pares e atualização do tabuleiro (tirando as cartas e pontuando)
        if tabuleiro[carta1] == tabuleiro[carta2]:
            print(f"O jogador {thread_id + 1} encontrou um par: {tabuleiro[carta1]}.")
            pontuacao[thread_id] += 1
            tabuleiro[carta1] = None
            tabuleiro[carta2] = None
            jogadas += 1
        else:
            print(f"O jogador {thread_id + 1} não encontrou um par.")

        semaforoTabuleiro.release()  # libera o tabuleiro após a jogada
        liberaTurno()
        time.sleep(random.uniform(0, 1))

# função: imprimindo o tabuleiro inicial
def imprimirTabuleiro():

    print("Bem-vindo ao Jogo da Memória!")
    print("Vos apresento o tabuleiro de cartas:")
    print("Boa sorte! :)")

    print()

    for i in range(0, len(tabuleiro), tamanhoTabuleiro):
        print(tabuleiro[i:i + tamanhoTabuleiro])
    print()

def main():

    imprimirTabuleiro()

    # criar e iniciar as threads
    threadPlayer1 = threading.Thread(target=jogar, args=(0,))
    threadPlayer2 = threading.Thread(target=jogar, args=(1,))


    threadPlayer1.start()
    threadPlayer2.start()

    # finalização
    threadPlayer1.join()
    threadPlayer2.join()


    # resultados:
    print("E a pontuação final é:")

    # impressão dos pontos e winner
    print(f'O Jogador 1 alcançou a pontuação: {pontuacao[0]}!')
    print(f'O Jogador 2 alcançou a pontuação: {pontuacao[1]}!')

    if pontuacao[0] > pontuacao[1]:
        print('Vence o Jogador 1. Parabéns! :)')
    elif pontuacao[1] > pontuacao[0]:
        print('Vence o Jogador 2. Parabéns! :)')
    else:
        print('O jogo terminou empatado! Parabéns aos jogadores! 🎉🥳')

if __name__ == "__main__":
    main()