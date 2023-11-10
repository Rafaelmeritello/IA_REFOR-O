from ambiente import Ambiente
from objeto import Objeto
from agente import Agente
from bandeira import Bandeira
from objetivo import Objetivo
import os
import random
from time import sleep
import uteis

input()
try:
    import matplotlib.pyplot as plt
except ImportError as err:
    print("Erro de importação:", err)
input()

exploration_rates = []
memory_sizes = []

rec_total = 0
desc_temporal = 1

exploracao = 0.99
FATOR_EXPLORACAO_DECAIMENTO = 0.9991
exploracao_minima = 0.20

DISTANCIA_PERTO = 1
MAX_ITENS = 7910
TEMPO_ESPERA = 0


# clear console
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


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


def testar_agente(agente, ambiente, estado):
    while True:
        cls()
        est_copy = estado.copy()
        acao = agente.escolher_acao(est_copy, exploracao)
        agente.realizar_acao(acao)

        estado = {
            "distancia_bandeira": ambiente.distancia(agente, bandeira),
            "distancia_objetivo": ambiente.distancia(agente, objetivo),
            "concluido": ambiente.concluido,
            "visao": ambiente.get_visao(DISTANCIA_PERTO, agente.get_posicao()),
            "bandeira_coletada": agente.bandeira_coletada,

        }

        # Exibir o estado do ambiente e o cenário
        print("Cenário:", ambiente.getcenario())
        print("Ação:", acao)
        print("Concluído:", estado["concluido"])
        print("Distância da bandeira:", estado["distancia_bandeira"])
        print("Distância do objetivo:", estado["distancia_objetivo"])
        print("Bandeira coletada:", estado["bandeira_coletada"])
        print("Visão:", estado["visao"])
        print("taxa_exploracao " + str(exploracao))
        print("-" * 20)

        # Use 0.8 segundos para o intervalo entre as ações
        if estado["concluido"]:
            rec_total = 0
            desc_temporal = 1

            ambiente.resetar()
            add_objetos(ambiente, agente.get_posicao())
            print("concluiu")
            sleep(4)

        sleep(0.8)


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
testar_agente(agente, ambiente, estado)
