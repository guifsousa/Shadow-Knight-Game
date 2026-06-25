import sys
import pygame

# Importa constantes de configuração da janela e opções do menu
from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION

# Importa as classes responsáveis pelas fases, menu e placar
from code.Level import Level
from code.Menu import Menu
from code.Score import Score


class Game:
    def __init__(self):
        # Inicializa todos os módulos do pygame
        pygame.init()

        # Cria a janela principal do jogo com as dimensões definidas em Const.py
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

        # Define o título exibido na barra da janela
        pygame.display.set_caption('Shadow Knight')

    def run(self):
        # Loop principal do jogo
        while True:

            # ── Exibe o menu principal ──

            # Cria o objeto Menu
            menu = Menu(self.window)

            # Executa o menu e recebe a opção escolhida pelo jogador
            menu_return = menu.run()

            # Verifica se foi escolhida alguma opção de iniciar jogo
            if menu_return in [MENU_OPTION[0], MENU_OPTION[1], MENU_OPTION[2]]:

                # Lista que armazenará a pontuação dos jogadores
                player_score = [0, 0]

                # Cria e inicia a primeira fase
                level = Level(
                    self.window,
                    'Level1',
                    menu_return,
                    player_score
                )

                # Executa a fase e recebe o resultado
                level_return = level.run(player_score)

                # Se o jogador venceu a fase 1
                if level_return:

                    # Cria e inicia a segunda fase
                    level = Level(
                        self.window,
                        'Level2',
                        menu_return,
                        player_score
                    )

                    # Executa a fase 2
                    level_return = level.run(player_score)

                    # Se venceu também a fase 2
                    if level_return:

                        # Cria o sistema de pontuação apenas após concluir o jogo
                        score = Score(self.window)

                        # Salva a pontuação final
                        score.save(menu_return, player_score)

                else:
                    # Caso o jogador perca, exibe a tela de Game Over
                    self._game_over()

            # Opção de visualizar ranking/placar
            elif menu_return == MENU_OPTION[3]:

                # Cria o objeto Score apenas quando necessário
                score = Score(self.window)

                # Exibe a tabela de pontuações
                score.show()

            # Opção de sair do jogo
            elif menu_return == MENU_OPTION[4]:

                # Encerra o pygame
                pygame.quit()

                # Finaliza a aplicação
                quit()

            # Qualquer retorno inesperado também encerra o jogo
            else:
                pygame.quit()
                sys.exit()

    def _game_over(self):
        """
        Exibe a tela de Game Over e aguarda o jogador pressionar
        qualquer tecla para retornar ao menu principal.
        """

        # Cria a fonte principal da mensagem
        font = pygame.font.SysFont(
            'garamondnegrito',
            52,
            bold=True
        )

        # Renderiza o texto GAME OVER
        text = font.render(
            'GAME OVER',
            True,
            (200, 0, 0)
        )

        # Centraliza o texto na tela
        rect = text.get_rect(
            center=(WIN_WIDTH // 2, WIN_HEIGHT // 2)
        )

        # Cria uma camada escura semitransparente sobre a tela
        overlay = pygame.Surface(
            (WIN_WIDTH, WIN_HEIGHT),
            pygame.SRCALPHA
        )

        # Define a cor preta com transparência
        overlay.fill((0, 0, 0, 180))

        # Desenha a camada escura
        self.window.blit(overlay, (0, 0))

        # Desenha o texto GAME OVER
        self.window.blit(text, rect)

        # Fonte utilizada para a mensagem auxiliar
        font_small = pygame.font.SysFont(
            'Lucida Sans Typewriter',
            16
        )

        # Texto informando como voltar ao menu
        sub = font_small.render(
            'Pressione qualquer tecla para voltar ao menu',
            True,
            (255, 255, 255)
        )

        # Centraliza a mensagem abaixo do GAME OVER
        sub_rect = sub.get_rect(
            center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)
        )

        # Desenha a mensagem auxiliar
        self.window.blit(sub, sub_rect)

        # Atualiza a tela exibindo todos os elementos
        pygame.display.flip()

        # Loop de espera até o usuário pressionar uma tecla
        while True:

            # Percorre os eventos do pygame
            for event in pygame.event.get():

                # Caso o usuário feche a janela
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Caso qualquer tecla seja pressionada
                if event.type == pygame.KEYDOWN:

                    # Retorna ao menu
                    return