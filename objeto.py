import ambiente


class Objeto:

    def __init__(self, representacao, ambiente, limite_movimento, colisao=False, passagem_liberada=False):
        self.__posicao = -1
        self.representacao = representacao
        self.ambiente = ambiente
        self.limite_movimento = limite_movimento
        self.colisao = colisao
        self.passagem_liberada = passagem_liberada

    def get_posicao(self):
        return self.__posicao

    def set_posicao(self, posicao):
        self.__posicao = posicao

    def _mover(self, passo):
        if (passo > self.limite_movimento or passo < -self.limite_movimento):
            passo = self.limite_movimento if passo > 0 else -self.limite_movimento
        self.ambiente.soliitar_movimento(self, self.__posicao + passo)

        self.ambiente.atualizar()

    def acionar(self):
        pass