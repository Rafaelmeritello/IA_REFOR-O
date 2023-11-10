from objeto import Objeto
import bandeira
import random


class Agente(Objeto):

    def __init__(self, representacao, ambiente):
        super().__init__(representacao, ambiente, 1)
        self.__probabilidades = []
        self.__acoes = ["direita", "esquerda", "soltar_esquerda", "soltar_direita"]
        self.__estado = None
        self.memoria = []
        self.objeto_colidido = None
        self.bandeira_coletada = False
        self.bandeira = None

    def add_acao(self, acao):
        self.__acoes.append(acao)

    def add_probabilidade(self, probabilidade):
        self.__probabilidades.append(probabilidade)

    def set_objeto_colidido(self, obj):
        if isinstance(obj, bandeira.Bandeira):
            self.bandeira_coletada = True
            self.bandeira = obj
        self.objeto_colidido = obj

    def get_objeto_colidido(self):
        return self.objeto_colidido

    def soltar_bandeira(self, direcao):
        if not self.bandeira_coletada:
            return False
        self.bandeira_coletada = False
        pos_bandeira = 0
        if direcao == "esquerda":
            pos_bandeira = self.get_posicao() - 1
            if pos_bandeira < 0: pos_bandeira = len(self.ambiente.getcenario()) - 1
        elif direcao == "direita":
            pos_bandeira = self.get_posicao() + 1
            if pos_bandeira > len(self.ambiente.getcenario()) - 1: pos_bandeira = 0
        self.ambiente.adicionar_objeto(pos_bandeira, self.bandeira)
        self.bandeira = None
        return True
        pass

    def realizar_acao(self, acao):
        if acao == "direita":
            super()._mover(1)
        elif acao == "esquerda":
            super()._mover(-1)
        elif acao == "soltar_direita":
            self.soltar_bandeira("direita")
        elif acao == "soltar_esquerda":
            self.soltar_bandeira("esquerda")
        else:
            raise Exception("Ação inválida")

    def escolher_acao(self, estado, prob_explo):
        rand = random.Random().random()

        if rand < prob_explo:
            return random.choice(self.__acoes)
        acao = ""
        possiveis = []

        for decisao in self.memoria:
            if decisao[0] == estado:
                possiveis.append(decisao)
                pass

        if (len(possiveis) == 0):
            return random.choice(self.__acoes)

        melhores = [possiveis[0]]
        for decisao in possiveis:
            if decisao[1] > melhores[0][1]:
                melhores = [decisao]
            if decisao[1] == melhores[0][1]:
                melhores.append(decisao)

        acao = random.choice(melhores)
        self.memoria = [decisao for decisao in self.memoria if (decisao[0] != estado) or (decisao[1] == melhores[0][1])]

        return acao[2]

    def registrar_memoria(self, estado, recompensa, acao):
        self.memoria.append((estado, recompensa, acao))

        # Limitar o tamanho da memória
        tamanho_limite = 21870
        if len(self.memoria) > tamanho_limite:

            if len(self.memoria) > tamanho_limite:
                self.memoria.pop(0)
