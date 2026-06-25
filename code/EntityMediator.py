from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Enemy import Enemy
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Player import Player
from code.PlayerShot import PlayerShot


# ── Classe responsável por gerenciar colisões entre entidades ──
# ── Funciona como um árbitro — verifica quem bateu em quem e aplica os efeitos ──
class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        # ── Verifica se a entidade saiu dos limites da tela e zera seu HP ──
        if ent is None:
            return

        # ── Inimigo saiu pela esquerda sem ser destruído ──
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0

        # ── Projétil do jogador saiu pela direita ──
        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0

        # ── Projétil do inimigo saiu pela esquerda ──
        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

        # ── Remove qualquer entidade que sair pelo topo ou fundo da tela ──
        if ent.rect.top >= WIN_HEIGHT or ent.rect.bottom <= 0:
            ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        # ── Verifica colisão entre dois pares de entidades válidos ──
        # ── Apenas interações que fazem sentido no jogo são processadas ──
        if ent1 is None or ent2 is None:
            return

        valid_interaction = False

        # ── Inimigo vs Projétil do Jogador ──
        if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
            valid_interaction = True
        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
            valid_interaction = True

        # ── Jogador vs Projétil do Inimigo ──
        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            valid_interaction = True
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            valid_interaction = True

        # ── Colisão direta Player vs Enemy ──
        elif isinstance(ent1, Player) and isinstance(ent2, Enemy):
            valid_interaction = True
        elif isinstance(ent1, Enemy) and isinstance(ent2, Player):
            valid_interaction = True

        if valid_interaction:
            # ── Verifica sobreposição real dos retângulos ──
            if ent1.rect.colliderect(ent2.rect):
                # ── Aplica dano mútuo entre as entidades ──
                ent1.health -= ent2.damage
                ent2.health -= ent1.damage
                # ── Registra quem causou o dano em cada entidade ──
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

    @staticmethod
    def __give_score(enemy: Enemy, entity_list):
        # ── Atribui pontos ao jogador que destruiu o inimigo ──
        # ── Verifica quem foi o último a causar dano usando last_dmg ──
        if enemy is None:
            return

        # ── Projétil do Jogador 1 destruiu o inimigo ──
        if enemy.last_dmg == 'Player1Shot':
            for ent in entity_list:
                if ent is not None and ent.name == 'Player1':
                    ent.score += enemy.score

        # ── Projétil do Jogador 2 destruiu o inimigo ──
        elif enemy.last_dmg == 'Player2Shot':
            for ent in entity_list:
                if ent is not None and ent.name == 'Player2':
                    ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list):
        # ── Remove entidades None da lista antes de processar ──
        entity_list[:] = [e for e in entity_list if e is not None]

        # ── Percorre todos os pares de entidades verificando colisões ──
        # ── Usa i+1 no loop interno para não checar o mesmo par duas vezes ──
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            # ── Verifica se a entidade saiu da tela ──
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                # ── Verifica colisão entre os dois ──
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list):
        # ── Remove entidades None da lista antes de processar ──
        entity_list[:] = [e for e in entity_list if e is not None]

        # ── Percorre cópia da lista para evitar erro ao remover durante iteração ──
        for ent in entity_list[:]:
            if ent.health <= 0:
                # ── Se for inimigo, distribui o score antes de remover ──
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)
                # ── Remove a entidade da lista ──
                entity_list.remove(ent)