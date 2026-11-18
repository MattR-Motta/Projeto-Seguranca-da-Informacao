"""Módulo de cadastro e autenticação segura de usuários."""
from .servico import autenticarUsuario, cadastrarUsuario, obterRegistroProtegido

__all__ = [
    "autenticarUsuario",
    "cadastrarUsuario",
    "obterRegistroProtegido",
]
