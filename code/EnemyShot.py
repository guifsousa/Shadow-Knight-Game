from code.Const import ENTITY_SPEED
from code.Entity import Entity


class EnemyShot(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self):
        # ── Move o projétil para a esquerda ──
        self.rect.centerx -= ENTITY_SPEED[self.name]
        # ── Remove quando sair da tela pela esquerda ──
        if self.rect.right < 0:
            self.health = 0