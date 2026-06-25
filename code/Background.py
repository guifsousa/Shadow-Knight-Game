import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, ENTITY_SPEED
from code.Entity import Entity


# ── Representa uma camada do fundo do cenário ──
# ── Herda de Entity para aproveitar o carregamento de imagem e posicionamento ──
class Background(Entity):

    def __init__(self, name: str, position: tuple):
        # ── Chama o construtor da classe Entity para carregar a imagem e definir posição ──
        super().__init__(name, position)

        # ── Redimensiona o fundo para cobrir toda a tela ──
        self.surf = pygame.transform.scale(
            self.surf,
            (WIN_WIDTH, WIN_HEIGHT)
        )

        # ── Redefine o retângulo de posição após o redimensionamento ──
        self.rect = self.surf.get_rect(
            left=position[0],
            top=position[1]
        )

    def move(self):
        # ── Move o fundo para a esquerda criando efeito de movimento ──
        # ── A velocidade é definida no Const.py para cada camada ──
        self.rect.centerx -= ENTITY_SPEED[self.name]

        # ── Quando a imagem sair completamente pela esquerda ──
        # ── reposiciona ela do lado direito para criar scroll infinito ──
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH