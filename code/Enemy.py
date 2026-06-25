from code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY
from code.EnemyShot import EnemyShot
from code.Entity import Entity


# ── Representa um inimigo do jogo ──
# ── Herda de Entity e adiciona movimento automático e sistema de tiro ──
class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        # ── Chama o construtor da Entity para carregar imagem e atributos ──
        super().__init__(name, position)
        # ── Inicializa o contador de delay do tiro com o valor definido no Const.py ──
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self):
        # ── Move o inimigo para a esquerda em direção ao jogador ──
        self.rect.centerx -= ENTITY_SPEED[self.name]
        # ── Zera o HP quando sair da tela pela esquerda para ser removido ──
        if self.rect.right < 0:
            self.health = 0

    def shoot(self):
        # ── Decrementa o contador de delay a cada frame ──
        self.shot_delay -= 1
        if self.shot_delay <= 0:
            # ── Reseta o delay multiplicado por 2 para dar espaço entre os tiros ──
            self.shot_delay = ENTITY_SHOT_DELAY[self.name] * 2
            # ── Cria e retorna um projétil na posição atual do inimigo ──
            # ── O nome do projétil é gerado automaticamente ex: 'Enemy1Shot' ──
            return EnemyShot(
                name=f'{self.name}Shot',
                position=(self.rect.centerx, self.rect.centery)
            )
        # ── Retorna None quando ainda não é hora de atirar ──
        return None