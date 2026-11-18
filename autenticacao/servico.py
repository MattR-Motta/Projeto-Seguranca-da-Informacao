import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)

from .armazenamento import conectarBanco


# Parâmetros explícitos para o Argon2id:
# 64 MiB de memória, 3 iterações, paralelismo 4 e salt aleatório de 16 bytes.
_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


def _validarCredenciais(nomeUsuario, senha):
    if not isinstance(nomeUsuario, str) or not nomeUsuario.strip():
        raise ValueError("Informe um nome de usuário.")

    if not isinstance(senha, str) or not senha:
        raise ValueError("Informe uma senha.")

    if len(senha) < 8:
        raise ValueError("A senha deve possuir pelo menos 8 caracteres.")


def cadastrarUsuario(nomeUsuario, senha, caminhoBanco=None):
    """Cadastra um usuário armazenando somente o hash Argon2id da senha."""
    _validarCredenciais(nomeUsuario, senha)
    nomeUsuario = nomeUsuario.strip()

    hashSenha = _hasher.hash(senha)

    conexao = conectarBanco(caminhoBanco)
    try:
        conexao.execute(
            "INSERT INTO usuarios (nomeUsuario, hashSenha) VALUES (?, ?)",
            (nomeUsuario, hashSenha),
        )
        conexao.commit()
    except sqlite3.IntegrityError as erro:
        conexao.rollback()
        if "UNIQUE constraint failed" in str(erro):
            raise ValueError("Este nome de usuário já está cadastrado.") from erro
        raise
    finally:
        conexao.close()

    return True


def autenticarUsuario(nomeUsuario, senha, caminhoBanco=None):
    """Valida as credenciais usando PasswordHasher.verify da biblioteca."""
    if not isinstance(nomeUsuario, str) or not nomeUsuario.strip():
        return False

    if not isinstance(senha, str) or not senha:
        return False

    conexao = conectarBanco(caminhoBanco)
    try:
        registro = conexao.execute(
            "SELECT hashSenha FROM usuarios WHERE nomeUsuario = ? COLLATE NOCASE",
            (nomeUsuario.strip(),),
        ).fetchone()
    finally:
        conexao.close()

    if registro is None:
        return False

    try:
        return _hasher.verify(registro["hashSenha"], senha)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def obterRegistroProtegido(nomeUsuario, caminhoBanco=None):
    """Retorna os dados não secretos e o hash para inspeção/evidência acadêmica."""
    if not isinstance(nomeUsuario, str) or not nomeUsuario.strip():
        return None

    conexao = conectarBanco(caminhoBanco)
    try:
        registro = conexao.execute(
            """
            SELECT nomeUsuario, hashSenha, criadoEm
            FROM usuarios
            WHERE nomeUsuario = ? COLLATE NOCASE
            """,
            (nomeUsuario.strip(),),
        ).fetchone()
    finally:
        conexao.close()

    return dict(registro) if registro else None