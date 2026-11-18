import tempfile
import unittest
from pathlib import Path

from autenticacao.servico import (
    autenticarUsuario,
    cadastrarUsuario,
    obterRegistroProtegido,
)


class TestesAutenticacao(unittest.TestCase):
    def setUp(self):
        self.pastaTemporaria = tempfile.TemporaryDirectory()
        self.caminhoBanco = Path(self.pastaTemporaria.name) / "usuarios_teste.db"

    def tearDown(self):
        self.pastaTemporaria.cleanup()

    def test_login_com_senha_correta(self):
        cadastrarUsuario("mateus", "SenhaSegura123", self.caminhoBanco)
        self.assertTrue(
            autenticarUsuario("mateus", "SenhaSegura123", self.caminhoBanco)
        )

    def test_login_com_senha_incorreta(self):
        cadastrarUsuario("mateus", "SenhaSegura123", self.caminhoBanco)
        self.assertFalse(
            autenticarUsuario("mateus", "SenhaErrada123", self.caminhoBanco)
        )

    def test_login_com_usuario_inexistente(self):
        self.assertFalse(
            autenticarUsuario("naoExiste", "SenhaSegura123", self.caminhoBanco)
        )

    def test_senha_nao_e_armazenada_em_texto_puro(self):
        senhaOriginal = "SenhaSegura123"
        cadastrarUsuario("mateus", senhaOriginal, self.caminhoBanco)

        registro = obterRegistroProtegido("mateus", self.caminhoBanco)

        self.assertIsNotNone(registro)
        self.assertNotEqual(registro["hashSenha"], senhaOriginal)
        self.assertTrue(registro["hashSenha"].startswith("$argon2id$"))
        self.assertNotIn(senhaOriginal, registro["hashSenha"])

    def test_cada_usuario_recebe_hash_com_salt_individual(self):
        cadastrarUsuario("usuario1", "SenhaSegura123", self.caminhoBanco)
        cadastrarUsuario("usuario2", "SenhaSegura123", self.caminhoBanco)

        registro1 = obterRegistroProtegido("usuario1", self.caminhoBanco)
        registro2 = obterRegistroProtegido("usuario2", self.caminhoBanco)

        self.assertNotEqual(registro1["hashSenha"], registro2["hashSenha"])

    def test_impede_usuario_duplicado(self):
        cadastrarUsuario("mateus", "SenhaSegura123", self.caminhoBanco)

        with self.assertRaises(ValueError):
            cadastrarUsuario("MATEUS", "OutraSenha123", self.caminhoBanco)

    def test_rejeita_senha_curta(self):
        with self.assertRaises(ValueError):
            cadastrarUsuario("mateus", "123", self.caminhoBanco)


if __name__ == "__main__":
    unittest.main(verbosity=2)