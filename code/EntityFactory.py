import random
from code.Background import Background
from code.Const import WIN_WIDTH, WIN_HEIGHT, GROUND_Y
from code.Enemy import Enemy
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str):
        match entity_name:

            # ── Cria o fundo com 4 camadas duplicadas para scroll infinito ──
            case 'Level1Bg' | 'Level2Bg':
                list_bg = []
                for i in range(4):
                    for x in (0, WIN_WIDTH):
                        list_bg.append(Background(f'{entity_name}{i}', (x, 0)))
                return list_bg

            # ── Player inicia no chão ──
            case 'Player1':
                return Player('Player1', (20, GROUND_Y - 56))

            case 'Player2':
                return Player('Player2', (60, GROUND_Y - 56))

            # ── Inimigos spawnam no chão pela direita ──
            case 'Enemy1':
                return Enemy('Enemy1', (WIN_WIDTH + 10, GROUND_Y - 48))

            case 'Enemy2':
                return Enemy('Enemy2', (WIN_WIDTH + 10, GROUND_Y - 56))

            case _:
                raise ValueError(f'EntityFactory: entidade "{entity_name}" não reconhecida.')