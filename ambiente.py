from objeto import Objeto
import agente
import objetivo


class Ambiente:

    def __init__(self, tamanho=11):
        self.__cenario = []
        self.objetos = []
        self.solicitacoes = []
        self.tamanho = tamanho
        self.concluido = False
        for i in range(0, self.tamanho):
            self.__cenario.append("#")

    def getcenario(self):
        return self.__cenario

    def resetar(self):
        for i in range(0, len(self.__cenario)):
            for objeto in self.objetos:
                if objeto.get_posicao() == i and not isinstance(objeto, agente.Agente):
                    self.__cenario[i] = "#"
                    self.objetos.remove(objeto)
            self.concluido = False

        self.concluido = False

    def get_visao(self, distancia, centro):
        visao = []
        for i in range(centro - distancia, centro + distancia + 1):
            if i < 0 or i > len(self.getcenario()) - 1:
                visao.append("-")
            else:
                visao.append(self.__cenario[i])
        return visao

    def adicionar_objeto(self, index, objeto):

        if self.__cenario[index] == "#":
            self.__cenario[index] = objeto.representacao
            objeto.set_posicao(index)
            self.objetos.append(objeto)
        else:
            for objetoI in self.objetos:
                if objetoI.get_posicao() == index:
                    objetoI.acionar(objeto)
                    if isinstance(objetoI, objetivo.Objetivo):
                        if objetoI.concluido == True:
                            self.concluido = True
                            break
            return False

    def distancia(self, obj1, obj2):
        pos1 = 0
        pos2 = 0
        for objeto in self.objetos:
            if objeto == obj1:
                pos1 = int(objeto.get_posicao())
                for objetoI in self.objetos:
                    if objetoI == obj2:
                        pos2 = int(objetoI.get_posicao())
        return pos1 - pos2

    def remover_objeto(self, index):
        if self.__cenario[index] != "#":
            self.__cenario[index] = "#"
            for objeto in self.objetos:
                if objeto.get_posicao() == index:
                    self.objetos.remove(objeto)
        else:
            return False

    def __mover_objeto(self, index_antigo, index_novo):
        if (index_novo >= len(self.__cenario)):
            index_novo = index_novo % len(self.__cenario)
        if (index_novo < 0):
            index_novo = (len(self.__cenario) - 1) - (index_novo * (-1)) + 1
        if self.__cenario[index_novo] == "#":
            self.__cenario[index_novo] = self.__cenario[index_antigo]
            self.__cenario[index_antigo] = "#"

            return index_novo
        else:

            for objeto in self.objetos:
                if not objeto.colisao and objeto.get_posicao() == index_novo:
                    colidido = objeto

                    if colidido.passagem_liberada:
                        index = index_novo - 1 if index_novo < index_antigo else index_novo + 1
                        return self.__mover_objeto(index_antigo, index)

                    for i in range(len(self.objetos)):
                        if isinstance(self.objetos[i], agente.Agente):
                            self.objetos[i].set_objeto_colidido(colidido)
                            self.remover_objeto(index_novo)
                            self.__cenario[index_novo] = self.__cenario[index_antigo]
                            self.__cenario[index_antigo] = "#"

                            return index_novo

            return -1

    def atualizar(self):

        for solicitacao in self.solicitacoes:
            mov = self.__mover_objeto(solicitacao[0].get_posicao(), solicitacao[1])
            if mov != -1:
                solicitacao[0].set_posicao(mov)
                self.solicitacoes.remove(solicitacao)

    def soliitar_movimento(self, objeto, pos_nova):
        self.solicitacoes.append((objeto, pos_nova))
