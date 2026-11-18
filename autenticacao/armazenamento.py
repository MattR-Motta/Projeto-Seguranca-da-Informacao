import sqlite3
from pathlib import Path


def obterCaminhoBanco():
    """Retorna o caminho padrão do banco de usuários."""
    return Path(__file__).resolve().parent.parent / "dados" / "usuarios.db"


def conectarBanco(caminhoBanco=None):
    """Abre o banco SQLite e garante a existência da tabela de usuários."""
    caminhoBanco = Path(caminhoBanco) if caminhoBanco else obterCaminhoBanco()
    caminhoBanco.parent.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(caminhoBanco)
    conexao.row_factory = sqlite3.Row
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomeUsuario TEXT NOT NULL COLLATE NOCASE UNIQUE,
            hashSenha TEXT NOT NULL,
            criadoEm TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conexao.commit()
    return conexao
