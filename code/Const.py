import pygame

# ---------------- CORES ----------------
# ── Tuplas RGB usadas para colorir textos e elementos visuais do jogo ──
C_ORANGE = (255, 128,   0)
C_YELLOW = (255, 255, 128)
C_WHITE  = (255, 255, 255)
C_GREEN  = (0,   128,   0)
C_CYAN   = (0,   128, 128)

# ---------------- TELA ----------------
# ── Dimensões da janela do jogo em pixels ──
WIN_WIDTH  = 576
WIN_HEIGHT = 324
# ── Posição Y do chão — usada para alinhar personagens ao chão do cenário ──
GROUND_Y   = 320

# ---------------- EVENTOS ----------------
# ── Eventos customizados do pygame disparados por timers ──
EVENT_ENEMY   = pygame.USEREVENT + 1  # ── dispara para criar um novo inimigo ──
EVENT_TIMEOUT = pygame.USEREVENT + 2  # ── dispara a cada 100ms para o contador ──

# ---------------- SPAWN ----------------
# ── Configurações de tempo da fase ──
SPAWN_TIME    = 1000   # ── cria inimigo a cada 1 segundo (ms) ──
TIMEOUT_STEP  = 100    # ── decrementa o timer a cada 100ms ──
TIMEOUT_LEVEL = 60000  # ── duração da fase: 60 segundos ──

# ---------------- MENU ----------------
# ── Opções exibidas no menu principal ──
MENU_OPTION = (
    'NEW GAME 1P',
    'NEW GAME 2P - COOPERATIVE',
    'NEW GAME 2P - COMPETITIVE',
    'SCORE',
    'EXIT'
)

# ---------------- ENTITY SPEED ----------------
# ── Velocidade em pixels por frame de cada entidade ──
# ── Backgrounds com velocidades diferentes criam o efeito parallax ──
ENTITY_SPEED = {
    # ── Camadas do fundo Level 1 — quanto maior, mais rápido e mais à frente ──
    'Level1Bg0':    0,  # ── fundo parado ──
    'Level1Bg1':    3,
    'Level1Bg2':    2,
    'Level1Bg3':    3,
    # ── Camadas do fundo Level 2 ──
    'Level2Bg0':    0,  # ── fundo parado ──
    'Level2Bg1':    1,
    'Level2Bg2':    2,
    'Level2Bg3':    3,
    # ── Jogadores ──
    'Player1':      3,
    'Player1Shot': 18,
    'Player2':      3,
    'Player2Shot': 18,
    # ── Inimigos ──
    'Enemy1':       3,
    'Enemy2':       3,
    'Enemy1Shot':   5,
    'Enemy2Shot':   5,
}

# ---------------- ENTITY HEALTH ----------------
# ── Pontos de vida iniciais de cada entidade ──
# ── Backgrounds têm 999 para nunca serem removidos ──
ENTITY_HEALTH = {
    'Level1Bg0': 999,
    'Level1Bg1': 999,
    'Level1Bg2': 999,
    'Level1Bg3': 999,
    'Level2Bg0': 999,
    'Level2Bg1': 999,
    'Level2Bg2': 999,
    'Level2Bg3': 999,
    'Player1':     300,
    'Player2':     300,
    'Player1Shot':  30,
    'Player2Shot':  20,
    'Enemy1Shot':    5,
    'Enemy2Shot':    3,
    'Enemy1':       50,
    'Enemy2':       60,
}

# ---------------- ENTITY DAMAGE ----------------
# ── Dano causado ao colidir com outra entidade ──
ENTITY_DAMAGE = {
    # ── Backgrounds não causam dano ──
    'Level1Bg0':  0,
    'Level1Bg1':  0,
    'Level1Bg2':  0,
    'Level1Bg3':  0,
    'Level2Bg0':  0,
    'Level2Bg1':  0,
    'Level2Bg2':  0,
    'Level2Bg3':  0,
    # ── Jogadores causam dano mínimo ao encostar ──
    'Player1':     1,
    'Player2':     1,
    # ── Projéteis causam dano alto ──
    'Player1Shot': 70,
    'Player2Shot': 20,
    'Enemy1Shot':  20,
    'Enemy2Shot':  15,
    # ── Inimigos causam dano mínimo ao encostar ──
    'Enemy1':       1,
    'Enemy2':       1,
}

# ---------------- PONTUAÇÃO ----------------
# ── Score ganho ao derrotar cada entidade ──
ENTITY_SCORE = {
    # ── Backgrounds e projéteis não dão pontos ──
    'Level1Bg0':  0,
    'Level1Bg1':  0,
    'Level1Bg2':  0,
    'Level1Bg3':  0,
    'Level2Bg0':  0,
    'Level2Bg1':  0,
    'Level2Bg2':  0,
    'Level2Bg3':  0,
    'Player1':     0,
    'Player2':     0,
    'Player1Shot': 0,
    'Player2Shot': 0,
    # ── Inimigos dão pontos ao serem derrotados ──
    'Enemy1':    100,
    'Enemy2':    125,
    'Enemy1Shot':  0,
    'Enemy2Shot':  0,
}

# ---------------- PROGRESSÃO DE FASE ----------------
# ── Score necessário para completar cada fase ──
LEVEL1_SCORE_LIMIT = 1000
LEVEL2_SCORE_LIMIT = 3000

# ---------------- COOLDOWN TIRO ----------------
# ── Delay em frames entre cada tiro — menor = atira mais rápido ──
ENTITY_SHOT_DELAY = {
    'Player1':  10,
    'Player2':  10,
    'Enemy1':   25,
    'Enemy2':   25,
}

# ---------------- CONTROLES ----------------
# ── Mapeamento de teclas para cada jogador ──
# ── Jogador 1: setas do teclado + SPACE ──
# ── Jogador 2: WASD + CTRL esquerdo ──
PLAYER_KEY_UP    = {'Player1': pygame.K_UP,    'Player2': pygame.K_w}
PLAYER_KEY_DOWN  = {'Player1': pygame.K_DOWN,  'Player2': pygame.K_s}
PLAYER_KEY_LEFT  = {'Player1': pygame.K_LEFT,  'Player2': pygame.K_a}
PLAYER_KEY_RIGHT = {'Player1': pygame.K_RIGHT, 'Player2': pygame.K_d}
PLAYER_KEY_SHOOT = {'Player1': pygame.K_SPACE, 'Player2': pygame.K_LCTRL}

# ---------------- POSIÇÃO SCORE ----------------
# ── Coordenadas centrais de cada linha da tela de score ──
SCORE_POS = {
    'Title':     (WIN_WIDTH / 2,  50),  # ── título ──
    'EnterName': (WIN_WIDTH / 2,  80),  # ── instrução para digitar nome ──
    'Label':     (WIN_WIDTH / 2,  90),  # ── cabeçalho da tabela ──
    'Name':      (WIN_WIDTH / 2, 110),  # ── nome digitado pelo jogador ──
    0: (WIN_WIDTH / 2, 110),  # ── 1º lugar ──
    1: (WIN_WIDTH / 2, 130),  # ── 2º lugar ──
    2: (WIN_WIDTH / 2, 150),  # ── 3º lugar ──
    3: (WIN_WIDTH / 2, 170),  # ── 4º lugar ──
    4: (WIN_WIDTH / 2, 190),  # ── 5º lugar ──
    5: (WIN_WIDTH / 2, 210),  # ── 6º lugar ──
    6: (WIN_WIDTH / 2, 230),  # ── 7º lugar ──
    7: (WIN_WIDTH / 2, 250),  # ── 8º lugar ──
    8: (WIN_WIDTH / 2, 270),  # ── 9º lugar ──
    9: (WIN_WIDTH / 2, 290),  # ── 10º lugar ──
}