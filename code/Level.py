import sys
import random
import pygame

# Importa tipos utilizados para tipagem e manipulação gráfica
from pygame import Surface, Rect
from pygame.font import Font

# Importa constantes do jogo
from code.Const import (
    C_WHITE,
    WIN_HEIGHT,
    WIN_WIDTH,
    MENU_OPTION,
    EVENT_ENEMY,
    SPAWN_TIME,
    C_GREEN,
    C_CYAN,
    LEVEL1_SCORE_LIMIT,
    LEVEL2_SCORE_LIMIT
)

# Importa classes utilizadas na fase
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    """
    Classe responsável por executar uma fase do jogo.
    Gerencia jogadores, inimigos, colisões, pontuação,
    renderização e condições de vitória ou derrota.
    """

    def __init__(
        self,
        window: Surface,
        name: str,
        game_mode: str,
        player_score: list[int]
    ):
        # Referência para a janela principal
        self.window = window

        # Nome da fase (Level1 ou Level2)
        self.name = name

        # Modo de jogo selecionado no menu
        self.game_mode = game_mode

        # Lista contendo todas as entidades da fase
        self.entity_list: list[Entity] = []

        # Adiciona o plano de fundo correspondente à fase
        self.entity_list.extend(
            EntityFactory.get_entity(self.name + 'Bg')
        )

        # Cria o Player1
        player = EntityFactory.get_entity('Player1')

        # Recupera a pontuação anterior do jogador
        player.score = player_score[0]

        # Adiciona o jogador na lista de entidades
        self.entity_list.append(player)

        # Caso seja modo para dois jogadores
        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:

            # Cria o Player2
            player = EntityFactory.get_entity('Player2')

            # Recupera sua pontuação anterior
            player.score = player_score[1]

            # Adiciona na fase
            self.entity_list.append(player)

    def run(self, player_score: list[int]):
        """
        Executa o loop principal da fase.
        Retorna:
        - True  -> vitória
        - False -> derrota
        """

        # Configura o evento periódico de geração de inimigos
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)

        # Carrega a música da fase
        pygame.mixer.music.load(f'./asset/{self.name}.mp3')

        # Define o volume da música
        pygame.mixer.music.set_volume(0.3)

        # Toca a música em loop infinito
        pygame.mixer.music.play(-1)

        # Relógio para controle de FPS
        clock = pygame.time.Clock()

        # Define a pontuação necessária para vencer
        target_score = (
            LEVEL1_SCORE_LIMIT
            if self.name == 'Level1'
            else LEVEL2_SCORE_LIMIT
        )

        # Loop principal da fase
        while True:

            # Limita o jogo a 60 FPS
            clock.tick(60)

            # Limpa a tela com a cor preta
            self.window.fill((0, 0, 0))

            # Percorre uma cópia da lista de entidades
            for ent in self.entity_list[:]:

                # Desenha a entidade na tela
                self.window.blit(ent.surf, ent.rect)

                # Atualiza seu movimento
                ent.move()

                # Apenas jogadores e inimigos podem atirar
                if isinstance(ent, (Player, Enemy)):

                    # Tenta criar um projétil
                    shoot = ent.shoot()

                    # Se um projétil foi criado
                    if shoot is not None:

                        # Adiciona-o à lista de entidades
                        self.entity_list.append(shoot)

                # Exibe informações do Player1
                if ent.name == 'Player1':
                    self.level_text(
                        14,
                        f'Player1 - Health: {ent.health} | Score: {ent.score}',
                        C_GREEN,
                        (10, 25)
                    )

                # Exibe informações do Player2
                if ent.name == 'Player2':
                    self.level_text(
                        14,
                        f'Player2 - Health: {ent.health} | Score: {ent.score}',
                        C_CYAN,
                        (10, 45)
                    )

            # Processa eventos do pygame
            for event in pygame.event.get():

                # Fechamento da janela
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Evento periódico de geração de inimigos
                if event.type == EVENT_ENEMY:

                    # Escolhe aleatoriamente um tipo de inimigo
                    choice = random.choice(
                        ('Enemy1', 'Enemy2')
                    )

                    # Cria e adiciona o inimigo à fase
                    self.entity_list.append(
                        EntityFactory.get_entity(choice)
                    )

            # ── Sistema de colisões ──

            # Verifica colisões entre entidades
            EntityMediator.verify_collision(
                self.entity_list
            )

            # Remove entidades sem vida
            EntityMediator.verify_health(
                self.entity_list
            )

            # ── Cálculo da pontuação atual ──

            current_score = 0

            # Procura a maior pontuação entre os jogadores
            for ent in self.entity_list:

                if isinstance(ent, Player):
                    current_score = max(
                        current_score,
                        ent.score
                    )

            # ── Interface da fase (HUD) ──

            # Exibe o progresso em direção ao objetivo
            self.level_text(
                14,
                f'Objetivo: {current_score}/{target_score}',
                C_WHITE,
                (10, 5)
            )

            # Exibe FPS atuais
            self.level_text(
                14,
                f'FPS: {clock.get_fps():.0f}',
                C_WHITE,
                (10, WIN_HEIGHT - 35)
            )

            # Exibe quantidade de entidades ativas
            self.level_text(
                14,
                f'Entidades: {len(self.entity_list)}',
                C_WHITE,
                (10, WIN_HEIGHT - 20)
            )

            # Atualiza toda a tela
            pygame.display.flip()

            # ── Verificação de derrota ──

            # Procura jogadores ainda vivos
            found_player = any(
                isinstance(ent, Player)
                for ent in self.entity_list
            )

            # Se não existir nenhum jogador
            if not found_player:

                # Desativa geração de inimigos
                pygame.time.set_timer(
                    EVENT_ENEMY,
                    0
                )

                # Retorna derrota
                return False

            # ── Verificação de vitória ──

            if current_score >= target_score:

                # Salva a pontuação atual dos jogadores
                for ent in self.entity_list:

                    if (
                        isinstance(ent, Player)
                        and ent.name == 'Player1'
                    ):
                        player_score[0] = ent.score

                    if (
                        isinstance(ent, Player)
                        and ent.name == 'Player2'
                    ):
                        player_score[1] = ent.score

                # Desativa geração de inimigos
                pygame.time.set_timer(
                    EVENT_ENEMY,
                    0
                )

                # Retorna vitória
                return True

    def level_text(
        self,
        text_size: int,
        text: str,
        text_color: tuple,
        text_pos: tuple
    ):
        """
        Método auxiliar para desenhar textos na tela.
        """

        # Cria a fonte desejada
        text_font: Font = pygame.font.SysFont(
            name="Lucida Sans Typewriter",
            size=text_size
        )

        # Renderiza o texto em uma superfície
        text_surf: Surface = text_font.render(
            text,
            True,
            text_color
        ).convert_alpha()

        # Define a posição onde o texto será desenhado
        text_rect: Rect = text_surf.get_rect(
            left=text_pos[0],
            top=text_pos[1]
        )

        # Desenha o texto na janela
        self.window.blit(
            text_surf,
            text_rect
        )