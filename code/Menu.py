import pygame

# Importa classes utilizadas para renderização de imagens, retângulos e textos
from pygame import Surface, Rect
from pygame.font import Font

# Importa constantes utilizadas pelo menu
from code.Const import (
    WIN_WIDTH,
    WIN_HEIGHT,
    C_ORANGE,
    MENU_OPTION,
    C_WHITE,
    C_YELLOW,
    C_GREEN
)


class Menu:
    """
    Classe responsável pela tela principal do jogo.

    Exibe o plano de fundo, opções disponíveis,
    recebe comandos do teclado e retorna a opção
    selecionada pelo jogador.
    """

    def __init__(self, window):
        # Referência para a janela principal do jogo
        self.window = window

        # Carrega a imagem de fundo do menu
        self.surf = pygame.image.load(
            './asset/MenuBg.png'
        ).convert_alpha()

        # Ajusta a imagem para ocupar toda a janela
        self.surf = pygame.transform.scale(
            self.surf,
            (WIN_WIDTH, WIN_HEIGHT)
        )

        # Cria o retângulo de posicionamento da imagem
        self.rect = self.surf.get_rect(
            left=0,
            top=0
        )

    def run(self):
        """
        Executa o loop principal do menu.

        Retorna a opção escolhida pelo jogador.
        """

        # Opção inicialmente selecionada
        menu_option = 0

        # Carrega a música do menu
        pygame.mixer.music.load('./asset/Menu.mp3')

        # Reproduz a música em loop infinito
        pygame.mixer.music.play(-1)

        # ── Desativa timers utilizados nas fases ──
        # Isso evita que eventos de inimigos continuem
        # acontecendo após retornar ao menu.
        pygame.time.set_timer(
            pygame.USEREVENT + 1,
            0
        )

        pygame.time.set_timer(
            pygame.USEREVENT + 2,
            0
        )

        # Loop principal do menu
        while True:

            # Desenha o plano de fundo
            self.window.blit(
                self.surf,
                self.rect
            )

            # ── Título do jogo ──

            self.menu_text(
                28,
                "SHADOW",
                C_ORANGE,
                (WIN_WIDTH / 2, 40)
            )

            self.menu_text(
                28,
                "KNIGHT",
                C_ORANGE,
                (WIN_WIDTH / 2, 75)
            )

            # ── Linha decorativa abaixo do título ──

            pygame.draw.line(
                self.window,
                C_YELLOW,
                (WIN_WIDTH // 2 - 80, 100),
                (WIN_WIDTH // 2 + 80, 100),
                1
            )

            pygame.draw.circle(
                self.window,
                C_YELLOW,
                (WIN_WIDTH // 2, 100),
                3
            )

            # ── Exibição das opções do menu ──

            for i in range(len(MENU_OPTION)):

                # Destaca a opção atualmente selecionada
                color = (
                    C_YELLOW
                    if i == menu_option
                    else C_WHITE
                )

                # Calcula a posição vertical do botão
                btn_y = 115 + 38 * i

                # Cria a área clicável/visual do botão
                btn_rect = pygame.Rect(
                    WIN_WIDTH // 2 - 140,
                    btn_y - 12,
                    280,
                    26
                )

                # Define a cor de fundo do botão
                btn_col = (
                    C_GREEN
                    if i == menu_option
                    else (101, 67, 33)
                )

                # Desenha o preenchimento do botão
                pygame.draw.rect(
                    self.window,
                    btn_col,
                    btn_rect,
                    border_radius=13
                )

                # Desenha a borda do botão
                pygame.draw.rect(
                    self.window,
                    C_YELLOW,
                    btn_rect,
                    1,
                    border_radius=13
                )

                # Desenha o texto da opção
                self.menu_text(
                    14,
                    MENU_OPTION[i],
                    color,
                    (WIN_WIDTH / 2, btn_y)
                )

            # ── Texto com instruções de controle ──

            self.menu_text(
                10,
                "UP/DOWN Navigate  |  ENTER Select",
                C_WHITE,
                (WIN_WIDTH / 2, WIN_HEIGHT - 10)
            )

            # Atualiza toda a tela
            pygame.display.flip()

            # Processa eventos do pygame
            for event in pygame.event.get():

                # Fechamento da janela
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Evento de teclado
                if event.type == pygame.KEYDOWN:

                    # Move a seleção para baixo
                    if event.key == pygame.K_DOWN:
                        menu_option = (
                            menu_option + 1
                        ) % len(MENU_OPTION)

                    # Move a seleção para cima
                    if event.key == pygame.K_UP:
                        menu_option = (
                            menu_option - 1
                        ) % len(MENU_OPTION)

                    # Confirma a seleção atual
                    if event.key == pygame.K_RETURN:

                        # Retorna a opção escolhida
                        return MENU_OPTION[menu_option]

    def menu_text(
        self,
        text_size,
        text,
        text_color,
        text_center_pos
    ):

        # Cria a fonte utilizada no menu
        text_font = pygame.font.SysFont(
            "Lucida Sans Typewriter",
            text_size
        )

        # Renderiza o texto em uma superfície
        text_surf = text_font.render(
            text,
            True,
            text_color
        ).convert_alpha()

        # Centraliza o texto na posição desejada
        text_rect = text_surf.get_rect(
            center=text_center_pos
        )

        # Desenha o texto na janela
        self.window.blit(
            text_surf,
            text_rect
        )