import pygame

# Importa constantes relacionadas à movimentação,
# limites da tela e controles dos jogadores
from code.Const import (
    ENTITY_SPEED,
    WIN_HEIGHT,
    WIN_WIDTH,
    PLAYER_KEY_UP,
    PLAYER_KEY_DOWN,
    PLAYER_KEY_LEFT,
    PLAYER_KEY_RIGHT,
    PLAYER_KEY_SHOOT,
    ENTITY_SHOT_DELAY
)

# Importa a classe base de todas as entidades do jogo
from code.Entity import Entity

# Importa a classe responsável pelos projéteis do jogador
from code.PlayerShot import PlayerShot


class Player(Entity):
    """
    Classe que representa os jogadores controlados
    pelo usuário.

    Herda da classe Entity e adiciona:
    - Movimentação via teclado;
    - Sistema de disparos;
    - Controle de intervalo entre tiros.
    """

    def __init__(self, name: str, position: tuple):
        # Inicializa os atributos herdados da classe Entity
        super().__init__(name, position)

        # Define o tempo de espera entre disparos
        # específico para cada jogador
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self):
        """
        Atualiza a posição do jogador de acordo
        com as teclas pressionadas.
        """

        # Obtém o estado atual de todas as teclas
        pressed_key = pygame.key.get_pressed()

        # Movimento para cima
        if (
            pressed_key[PLAYER_KEY_UP[self.name]]
            and self.rect.top > 0
        ):
            self.rect.centery -= ENTITY_SPEED[self.name]

        # Movimento para baixo
        if (
            pressed_key[PLAYER_KEY_DOWN[self.name]]
            and self.rect.bottom < WIN_HEIGHT
        ):
            self.rect.centery += ENTITY_SPEED[self.name]

        # Movimento para esquerda
        if (
            pressed_key[PLAYER_KEY_LEFT[self.name]]
            and self.rect.left > 0
        ):
            self.rect.centerx -= ENTITY_SPEED[self.name]

        # Movimento para direita
        if (
            pressed_key[PLAYER_KEY_RIGHT[self.name]]
            and self.rect.right < WIN_WIDTH
        ):
            self.rect.centerx += ENTITY_SPEED[self.name]

    def shoot(self):
        """
        Controla os disparos do jogador.

        Utiliza um contador (shot_delay) para limitar
        a frequência de tiros.
        """

        # Reduz o contador de espera a cada frame
        self.shot_delay -= 1

        # Quando o contador chega a zero,
        # o jogador pode tentar disparar novamente
        if self.shot_delay == 0:

            # Reinicia o contador para o próximo disparo
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]

            # Verifica quais teclas estão pressionadas
            pressed_key = pygame.key.get_pressed()

            # Se a tecla de tiro estiver pressionada
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:

                # Cria e retorna um novo projétil
                return PlayerShot(
                    name=f'{self.name}Shot',
                    position=(
                        self.rect.centerx,
                        self.rect.centery
                    )
                )

        # Caso não tenha disparado, retorna None
        return None