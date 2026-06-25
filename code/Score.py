import sys

# Utilizado para registrar data e hora da pontuação
from datetime import datetime

import pygame

# Importa classes e constantes do pygame
from pygame import (
    Surface,
    Rect,
    KEYDOWN,
    K_RETURN,
    K_BACKSPACE,
    K_ESCAPE
)

from pygame.font import Font

# Importa constantes utilizadas na tela de score
from code.Const import (
    C_YELLOW,
    SCORE_POS,
    MENU_OPTION,
    C_WHITE,
    WIN_WIDTH,
    WIN_HEIGHT
)

# Classe responsável pela comunicação com o banco de dados
from code.DBProxy import DBProxy


class Score:
    """
    Classe responsável pelas telas de pontuação.

    Possui duas funções principais:
    - Salvar uma nova pontuação após a vitória;
    - Exibir o ranking Top 10.
    """

    def __init__(self, window: Surface):

        # Referência para a janela principal do jogo
        self.window = window

        # Carrega a imagem de fundo da tela de score
        self.surf = pygame.image.load(
            './asset/ScoreBg.png'
        ).convert_alpha()

        # Ajusta a imagem ao tamanho da janela
        self.surf = pygame.transform.scale(
            self.surf,
            (WIN_WIDTH, WIN_HEIGHT)
        )

        # Cria o retângulo de posicionamento do fundo
        self.rect = self.surf.get_rect(
            left=0,
            top=0
        )

    def save(self, game_mode: str, player_score: list[int]):
        """
        Exibe a tela de vitória e solicita um nome
        para salvar a pontuação no banco de dados.
        """

        # ── Música da tela de score ──
        pygame.mixer.music.load('./asset/Score.mp3')
        pygame.mixer.music.play(-1)

        # Cria conexão com o banco de dados
        db_proxy = DBProxy('DBScore.db')

        # Nome digitado pelo jogador
        name = ''

        while True:

            # Desenha o fundo da tela
            self.window.blit(
                self.surf,
                self.rect
            )

            # Exibe mensagem de vitória
            self.score_text(
                48,
                'YOU WIN!!',
                C_YELLOW,
                SCORE_POS['Title']
            )

            # Texto e pontuação padrão
            text = 'Enter Player 1 name (4 characters):'
            score = player_score[0]

            # ── Modo cooperativo ──
            if game_mode == MENU_OPTION[1]:

                # Média dos dois jogadores
                score = int(
                    (player_score[0] + player_score[1]) / 2
                )

                text = 'Enter Team name (4 characters):'

            # ── Modo versus ──
            elif game_mode == MENU_OPTION[2]:

                # Verifica quem teve a maior pontuação
                if player_score[0] >= player_score[1]:

                    score = player_score[0]

                    text = (
                        'Enter Player 1 name '
                        '(4 characters):'
                    )

                else:

                    score = player_score[1]

                    text = (
                        'Enter Player 2 name '
                        '(4 characters):'
                    )

            # Exibe instrução de digitação
            self.score_text(
                20,
                text,
                C_WHITE,
                SCORE_POS['EnterName']
            )

            # Exibe o nome digitado até o momento
            self.score_text(
                20,
                name,
                C_WHITE,
                SCORE_POS['Name']
            )

            # Atualiza a tela
            pygame.display.flip()

            # Processa eventos
            for event in pygame.event.get():

                # Fechamento da janela
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Evento de teclado
                elif event.type == KEYDOWN:

                    # Salva quando ENTER for pressionado
                    # e o nome possuir exatamente 4 caracteres
                    if (
                        event.key == K_RETURN
                        and len(name) == 4
                    ):

                        # Salva no banco de dados
                        db_proxy.save({
                            'name': name,
                            'score': score,
                            'date': get_formatted_date()
                        })

                        # Fecha conexão
                        db_proxy.close()

                        # Exibe ranking
                        self.show()

                        return

                    # Remove o último caractere digitado
                    elif event.key == K_BACKSPACE:

                        name = name[:-1]

                    # Adiciona caracteres ao nome
                    else:

                        if len(name) < 4:

                            name += (
                                event.unicode.upper()
                            )

    def show(self):
        """
        Exibe o ranking Top 10 armazenado
        no banco de dados.
        """

        # ── Música da tela de score ──
        pygame.mixer.music.load('./asset/Score.mp3')
        pygame.mixer.music.play(-1)

        # Conecta ao banco
        db_proxy = DBProxy('DBScore.db')

        # Recupera os 10 melhores registros
        list_score = db_proxy.retrieve_top10()

        # Fecha conexão
        db_proxy.close()

        while True:

            # Desenha o fundo
            self.window.blit(
                self.surf,
                self.rect
            )

            # Título do ranking
            self.score_text(
                48,
                'TOP 10 SCORE',
                C_YELLOW,
                SCORE_POS['Title']
            )

            # Cabeçalho da tabela
            self.score_text(
                20,
                'NAME     SCORE           DATE',
                C_YELLOW,
                SCORE_POS['Label']
            )

            # Percorre todos os registros retornados
            for i, player_score in enumerate(list_score):

                # Recupera os dados da linha
                name, score, date = player_score

                # Exibe a pontuação formatada
                self.score_text(
                    20,
                    f'{name}     {score:05d}     {date}',
                    C_YELLOW,
                    SCORE_POS[i]
                )

            # Atualiza a tela
            pygame.display.flip()

            # Processa eventos
            for event in pygame.event.get():

                # Fechamento da janela
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Evento de teclado
                if event.type == KEYDOWN:

                    # ENTER ou ESC retornam ao menu
                    if event.key in (
                        K_ESCAPE,
                        K_RETURN
                    ):
                        return

    def score_text(
        self,
        text_size: int,
        text: str,
        text_color: tuple,
        text_center_pos: tuple
    ):
        """
        Método auxiliar responsável por desenhar
        textos centralizados na tela.
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

        # Centraliza o texto na posição desejada
        text_rect: Rect = text_surf.get_rect(
            center=text_center_pos
        )

        # Desenha o texto na tela
        self.window.blit(
            source=text_surf,
            dest=text_rect
        )


def get_formatted_date():
    """
    Retorna a data e hora atual formatadas
    para armazenamento no ranking.
    """

    # Obtém data e hora atuais do sistema
    current_datetime = datetime.now()

    # Formata a hora
    current_time = current_datetime.strftime("%H:%M")

    # Formata a data
    current_date = current_datetime.strftime("%d/%m/%y")

    # Retorna tudo em uma única string
    return f"{current_time} - {current_date}"