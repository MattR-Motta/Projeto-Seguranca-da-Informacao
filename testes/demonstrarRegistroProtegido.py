import secrets
import tempfile
from pathlib import Path

from autenticacao.servico import cadastrarUsuario, obterRegistroProtegido


def demonstrarRegistroProtegido():
    with tempfile.TemporaryDirectory() as pastaTemporaria:
        caminhoBanco = Path(pastaTemporaria) / "evidencia.db"
        senhaDemonstracao = secrets.token_urlsafe(18)
        cadastrarUsuario(
            "usuario demonstracao",
            senhaDemonstracao,
            caminhoBanco,
        )
        registro = obterRegistroProtegido(
            "usuario demonstracao",
            caminhoBanco,
        )

        print("=== EVIDÊNCIA DE REGISTRO PROTEGIDO ===")
        print(f"Usuário: {registro['nomeUsuario']}")
        print(f"Hash armazenado: {registro['hashSenha']}")
        print(f"Criado em: {registro['criadoEm']}")
        print("Senha original armazenada: NÃO")
        print("Formato do hash: Argon2id (PHC)")
        print("Banco temporário: removido ao finalizar a demonstração.")


if __name__ == "__main__":
    demonstrarRegistroProtegido()