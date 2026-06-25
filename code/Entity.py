from abc import ABC, abstractmethod
import pygame
from code.Const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE, ENTITY_SPEED


# ── Dicionário que define o tamanho em pixels de cada entidade na tela ──
# ── Backgrounds não estão aqui pois são redimensionados pelo Background.py ──
ENTITY_SIZE = {
    'Player1':     (56, 56),
    'Player2':     (56, 56),
    'Player1Shot': (20,  8),
    'Player2Shot': (20,  8),
    'Enemy1':      (48, 48),
    'Enemy2':      (56, 56),
    'Enemy1Shot':  (20,  8),
    'Enemy2Shot':  (20,  8),
}


# ── Classe base abstrata de todas as entidades do jogo ──
# ── Não pode ser instanciada diretamente — serve como molde para Player, Enemy, etc. ──
class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        # ── Guarda o nome da entidade para identificação no jogo ──
        self.name = name

        # ── Carrega a imagem da entidade da pasta asset/ ──
        # ── convert_alpha() otimiza a imagem para renderização com transparência ──
        self.surf = pygame.image.load(f'./asset/{name}.png').convert_alpha()

        # ── Redimensiona a imagem se o nome estiver no dicionário ENTITY_SIZE ──
        # ── Backgrounds não são redimensionados aqui ──
        if name in ENTITY_SIZE:
            self.surf = pygame.transform.scale(self.surf, ENTITY_SIZE[name])

        # ── Define o retângulo de posição da entidade na tela ──
        self.rect       = self.surf.get_rect(left=position[0], top=position[1])

        # ── Atributos da entidade carregados do Const.py ──
        self.speed      = ENTITY_SPEED.get(self.name, 0)   # ── velocidade de movimento ──
        self.health     = ENTITY_HEALTH[self.name]          # ── vida atual ──
        self.max_health = ENTITY_HEALTH[self.name]          # ── vida máxima para barra de HP ──
        self.damage     = ENTITY_DAMAGE[self.name]          # ── dano causado ao colidir ──
        self.score      = ENTITY_SCORE[self.name]           # ── pontos dados ao ser derrotado ──
        self.last_dmg   = 'None'                            # ── nome da última entidade que causou dano ──

    # ── Método abstrato obrigatório em todas as classes filhas ──
    # ── Cada entidade deve implementar sua própria lógica de movimento ──
    @abstractmethod
    def move(self):
        pass