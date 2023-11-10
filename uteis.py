from ambiente import Ambiente
from objeto import Objeto
from agente import Agente
from bandeira import Bandeira
from objetivo import Objetivo

DISTANCIA_PERTO = 2
PENALIDADE_DISTANCIA_PERTO = 3
PENALIDADE_DISTANCIA_PADRAO = 2
FATOR_PENALIDADE_DISTANCIA = 0.9999
FATOR_RECOMPENSA_DISTANCIA = 1.0001
PENALIDADE_ALTA_ACAO = 15
RECOMPENSA_ALTA_PEGAR_BANDEIRA = 23
RECOMPENSA_ALTA_CONCLUIR = 28
PENALIDADE_ALTA_SOLTAR_SEM_CONCLUIR = 20
PENALIDADE_ALTA_SOLTAR_SEM_TER = 14


def calcula_recompensa(estado_antes,
                       estado_depois,
                       acao,
                       desc_temporal=1.00):
    reco = 0

    # Se ele não pegou nem tem a bandeira
    if not estado_antes["bandeira_coletada"] and not estado_depois[
        "bandeira_coletada"]:
        # Se se distanciou
        distancia_antes = abs(estado_antes["distancia_bandeira"])
        distancia_depois = abs(estado_depois["distancia_bandeira"])

        if distancia_antes < distancia_depois:
            if distancia_antes < DISTANCIA_PERTO:
                reco -= PENALIDADE_DISTANCIA_PERTO * desc_temporal
            else:
                reco -= PENALIDADE_DISTANCIA_PADRAO * desc_temporal
            desc_temporal *= FATOR_PENALIDADE_DISTANCIA
        elif distancia_antes > distancia_depois:
            reco += 10 * desc_temporal
            desc_temporal *= FATOR_RECOMPENSA_DISTANCIA

        # Fim - se se distanciou

        if acao == "soltar_direita" or acao == "soltar_esquerda":
            reco -= PENALIDADE_ALTA_SOLTAR_SEM_TER * desc_temporal

    # Fim -  se ele não pegou nem tem a bandeira

    # Se ele pegou a bandeira
    if estado_depois[
        "bandeira_coletada"] and not estado_antes["bandeira_coletada"]:
        reco += RECOMPENSA_ALTA_PEGAR_BANDEIRA * desc_temporal
        desc_temporal *= FATOR_PENALIDADE_DISTANCIA

    # Fim - se ele pegou a bandeira
    if estado_antes["bandeira_coletada"] and not estado_depois["bandeira_coletada"]:
        if estado_depois["concluido"]:
            reco += RECOMPENSA_ALTA_CONCLUIR * desc_temporal
            desc_temporal *= FATOR_PENALIDADE_DISTANCIA
        else:
            reco -= PENALIDADE_ALTA_SOLTAR_SEM_CONCLUIR * desc_temporal
            desc_temporal *= FATOR_PENALIDADE_DISTANCIA
    # Se ele esta com a a bandeira

    if estado_antes["bandeira_coletada"] and estado_depois["bandeira_coletada"]:
        # Se se aproximou do objetivo
        distancia_antes_objetivo = abs(estado_antes["distancia_objetivo"])
        distancia_depois_objetivo = abs(estado_depois["distancia_objetivo"])

        if distancia_antes_objetivo > distancia_depois_objetivo:
            reco += (10 - distancia_depois_objetivo) * desc_temporal
            desc_temporal *= FATOR_RECOMPENSA_DISTANCIA
        elif distancia_antes_objetivo < distancia_depois_objetivo:
            reco -= (10 - distancia_depois_objetivo) * desc_temporal
            desc_temporal *= FATOR_PENALIDADE_DISTANCIA
    return (reco, desc_temporal)
