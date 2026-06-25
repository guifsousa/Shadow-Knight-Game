import sqlite3


# ── Classe responsável por salvar e recuperar scores no banco de dados SQLite ──
# ── SQLite é um banco de dados local que salva tudo em um único arquivo .db ──
class DBProxy:
    def __init__(self, db_name: str):
        # ── Guarda o nome do banco e conecta ao arquivo .db ──
        # ── Se o arquivo não existir, o SQLite cria automaticamente ──
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)

        # ── Cria a tabela de scores se ainda não existir ──
        # ── IF NOT EXISTS garante que dados salvos anteriormente não são apagados ──
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS dados(
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT    NOT NULL,
                score INTEGER NOT NULL,
                date  TEXT    NOT NULL
            )
        ''')
        # ── Confirma a criação da tabela no banco ──
        self.connection.commit()

    def save(self, score_dict: dict):
        # ── Insere um novo registro de score no banco ──
        # ── score_dict deve conter as chaves: name, score, date ──
        # ── Exemplo: {'name': 'HERO', 'score': 1500, 'date': '14:30 - 01/01/25'} ──
        self.connection.execute(
            'INSERT INTO dados (name, score, date) VALUES (:name, :score, :date)',
            score_dict
        )
        # ── Confirma a inserção no banco ──
        self.connection.commit()

    def retrieve_top10(self) -> list:
        # ── Busca os 10 maiores scores em ordem decrescente ──
        # ── Retorna lista de tuplas: (name, score, date) ──
        # ── Usado pela tela de Score para exibir o ranking ──
        return self.connection.execute(
            'SELECT name, score, date FROM dados ORDER BY score DESC LIMIT 10'
        ).fetchall()

    def close(self):
        # ── Fecha a conexão com o banco ao terminar de usar ──
        # ── Importante para não corromper o arquivo .db ──
        self.connection.close()