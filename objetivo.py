from objeto import Objeto
import bandeira


class Objetivo(Objeto):

    def __init__(self, representacao, ambiente):
        super().__init__(representacao, ambiente, 0, passagem_liberada=True)
        self.concluido = False

    def resetar(self):
        self.concluido = False

    def acionar(self, objeto):
        if isinstance(objeto, bandeira.Bandeira):
            self.concluido = True

