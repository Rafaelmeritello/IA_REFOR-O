from ambiente import Ambiente
from objeto import Objeto
from agente import Agente
from bandeira import Bandeira
from objetivo import Objetivo
import os
import random
from time import sleep
import uteis
import pygame


running = True
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
VERDE = (0, 255, 0)

try:
    import matplotlib.pyplot as plt
except ImportError as err:
    print("Erro de importação:", err)


exploration_rates = []
memory_sizes = []

rec_total = 0
desc_temporal = 1

exploracao = 0.98
FATOR_EXPLORACAO_DECAIMENTO = 0.9991
exploracao_minima = 0.20

DISTANCIA_PERTO = 1
MAX_ITENS = 8110
TEMPO_ESPERA = 0


# clear console
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

#add objetos
def add_objetos(ambiente, pos_agente=5):
    pos_bandeira = random.randint(0, len(ambiente.getcenario()) - 1)
    pos_objetivo = random.randint(0, len(ambiente.getcenario()) - 1)

    while pos_objetivo == pos_bandeira or pos_objetivo == pos_agente or pos_bandeira == pos_agente or pos_objetivo == 10 or pos_objetivo == 0:
        pos_bandeira = random.randint(0, len(ambiente.getcenario()) - 1)
        pos_objetivo = random.randint(0, len(ambiente.getcenario()) - 1)

    ambiente.adicionar_objeto(pos_bandeira, bandeira)
    ambiente.adicionar_objeto(pos_objetivo, objetivo)


cls()
ambiente = Ambiente()

agente = Agente("A", ambiente)

ambiente.adicionar_objeto(5, agente)
bandeira = Bandeira("B", ambiente)
objetivo = Objetivo("O", ambiente)
add_objetos(ambiente)

estado = {
    "distancia_bandeira": ambiente.distancia(agente, bandeira),
    "distancia_objetivo": ambiente.distancia(agente, objetivo),
    "concluido": ambiente.concluido,
    "visao": ambiente.get_visao(DISTANCIA_PERTO, agente.get_posicao()),
    "bandeira_coletada": agente.bandeira_coletada,
}




#teste do agente
TAMANHO_BLOCO = 65
LARGURA_TELA = 800  # Ajuste conforme necessário

# Criar a janela Pygame uma vez antes do loop principal
LARGURA_TELA = 800  # Ajuste conforme necessário


def desenhar_cenario(ambiente, screen, conclusao=False):
    # Calcular a posição inicial para centralizar os blocos na tela
    posicao_inicial_x = (LARGURA_TELA - len(ambiente.getcenario()[0]) * TAMANHO_BLOCO) // 2
    posicao_x = posicao_inicial_x  # Definir a posição horizontal inicial

    for y, linha in enumerate(ambiente.getcenario()):
        for celula in linha:
            cor = BRANCO  # Cor padrão para células vazias
            if celula == "A":
                cor = AZUL  # Agente em azul
            elif celula == "B":
                cor = AMARELO  # Bandeira em amarelo
            elif celula == "O":
                cor = VERDE  # Objetivo em verde

            if conclusao:
                cor = VERDE  # Tornar todos os blocos verdes em caso de conclusão

            pygame.draw.rect(screen, cor, (posicao_x - 320, screen.get_height() / 2, TAMANHO_BLOCO, TAMANHO_BLOCO))

            # Incrementar a posição horizontal para o próximo bloco
            posicao_x += TAMANHO_BLOCO

    pygame.display.flip()

def testar_agente(agente, ambiente, estado, screen):
    pygame.init()
    exploracao = 0.14
    conclusao_timer = 0  # Contador para rastrear o tempo desde a conclusão
    conclusao_duration = 3  # Duração em segundos para mostrar todos os blocos verdes após a conclusão

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        est_copy = estado.copy()
        acao = agente.escolher_acao(est_copy, exploracao)
        sleep(0.22)
        agente.realizar_acao(acao)

        estado = {
            "distancia_bandeira": ambiente.distancia(agente, bandeira),
            "distancia_objetivo": ambiente.distancia(agente, objetivo),
            "concluido": ambiente.concluido,
            "visao": ambiente.get_visao(DISTANCIA_PERTO, agente.get_posicao()),
            "bandeira_coletada": agente.bandeira_coletada,
        }

        # Desenhar o cenário no Pygame
        desenhar_cenario(ambiente, screen, conclusao=estado["concluido"])

        if estado["concluido"]:
            rec_total = 0
            desc_temporal = 1

            ambiente.resetar()
            add_objetos(ambiente, agente.get_posicao())
            sleep(0.75)
            conclusao_timer = pygame.time.get_ticks() / 1000  # Obter o tempo atual em segundos

        if conclusao_timer > 0 and pygame.time.get_ticks() / 1000 - conclusao_timer > conclusao_duration:
            # Resetar o timer após a duração especificada
            conclusao_timer = 0

        sleep(0.1)
#treinamento
for i in range(MAX_ITENS):

    est_copy = estado.copy()
    print("visão do individuo: " + str(estado["visao"]))
    acao = agente.escolher_acao(est_copy, exploracao)

    print(ambiente.getcenario())
    agente.realizar_acao(acao)

    estado = {
        "distancia_bandeira": ambiente.distancia(agente, bandeira),
        "distancia_objetivo": ambiente.distancia(agente, objetivo),
        "concluido": ambiente.concluido,
        "visao": ambiente.get_visao(DISTANCIA_PERTO, agente.get_posicao()),
        "bandeira_coletada": agente.bandeira_coletada,
    }

    rec = uteis.calcula_recompensa(est_copy, estado, acao,
                                   desc_temporal)
    rec_total += rec[0]
    agente.registrar_memoria(est_copy, rec[0], acao)

    desc_temporal = rec[1]
    sleep(TEMPO_ESPERA)
    if estado["concluido"]:
        rec_total = 0
        desc_temporal = 1

        ambiente.resetar()
        add_objetos(ambiente, agente.get_posicao())
        print("concluiu")

    else:
        if exploracao > exploracao_minima:
            exploracao *= FATOR_EXPLORACAO_DECAIMENTO
    exploration_rates.append(exploracao*100)
    memory_sizes.append(len(agente.memoria))
    cls()
plt.figure(figsize=(10, 6))
plt.plot(range(MAX_ITENS), exploration_rates, label='Taxa de Exploração')
plt.plot(range(MAX_ITENS), memory_sizes, label='Taxa aprendizado')
plt.xlabel('Iteração de Treinamento')
plt.ylabel('Valor')
plt.legend()
plt.grid()
plt.title('Evolução da Taxa de Exploração e Taxa aprendizado')
plt.show()
screen = pygame.display.set_mode((LARGURA_TELA, 720))
testar_agente(agente, ambiente, estado,screen)

