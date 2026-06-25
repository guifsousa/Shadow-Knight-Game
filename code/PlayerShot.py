# Importa constantes utilizadas pelo projétil
from code.Const import ENTITY_SPEED, WIN_WIDTH

# Importa a classe base de entidades do jogo
from code.Entity import Entity


class PlayerShot(Entity):
    """
    Classe responsável pelos projéteis disparados
    pelos jogadores.

    Herda da classe Entity e possui apenas a lógica
    de movimentação do tiro.
    """

    def __init__(self, name: str, position: tuple):
        # Inicializa os atributos herdados da classe Entity
        super().__init__(name, position)

    def move(self):
        """
        Atualiza a posição do projétil a cada frame.
        """

        # ── Move o projétil para a direita ──
        # A velocidade utilizada depende do valor
        # configurado para este tipo de entidade.
        self.rect.centerx += ENTITY_SPEED[self.name]

        # ── Remove quando sair da tela ──
        # Quando o lado esquerdo do projétil ultrapassa
        # a largura da janela, ele não está mais visível.
        if self.rect.left > WIN_WIDTH:

            # Define a vida como zero para que o sistema
            # de verificação remova a entidade da fase.
            self.health = 0