import base64
from getpass import getpass
from criptografia import criptografarMensagem
from descriptografia import descriptografarMensagem


def testesIntegridade(senhaChavePrivada):
    """
    Executa testes para verificar a integridade da mensagem.

    Primeiro verifica se uma mensagem legítima pode ser recuperada.
    Depois altera os dados criptografados e verifica se a adulteração
    é detectada durante a descriptografia.
    """

    mensagemOriginal = ("Mensagem de teste")
    # TESTE 1: criptografia e descriptografia sem adulteração
    print("\n=== TESTE 1: MENSAGEM ORIGINAL ===")
    dadosCriptografados = criptografarMensagem(mensagemOriginal)
    mensagemRecuperada = descriptografarMensagem(dadosCriptografados,senhaChavePrivada)

    if mensagemRecuperada == mensagemOriginal:
        print("[SUCESSO] A mensagem foi recuperada corretamente.")
    else:
        raise AssertionError("A mensagem recuperada é diferente da mensagem original.")

    # TESTE 2: adulteração dos dados criptografados
    print("\n=== TESTE 2: DETECÇÃO DE ADULTERAÇÃO ===")
    # cria uma cópia para preservar os dados originais
    dadosAdulterados = dadosCriptografados.copy()
    # decodifica o conteudo criptografdo de base64 para bytes
    mensagemBytes = bytearray(base64.b64decode(dadosAdulterados["mensagemCriptografada"],validate=True))
    # altera um byte do conteúdo criptografado
    mensagemBytes[0] ^= 1
    # codifica novamente o conteúdo adulterado em Base64
    dadosAdulterados["mensagemCriptografada"] = (base64.b64encode(mensagemBytes).decode("utf-8"))
    try:
        # tenta descriptografar a mensagem adulterada
        descriptografarMensagem(dadosAdulterados,senhaChavePrivada)

    except ValueError as erro:
        # confirma que a falha ocorreu na autenticação do AES-GCM
        if "Falha na autenticação!" not in str(erro):
            raise

        print("[SUCESSO] A adulteração foi detectada!")
        print(f"Motivo: {erro}")

    else:
        raise AssertionError("ERRO: a mensagem adulterada foi aceita pelo sistema.")
    return {
        "testeMensagemOriginal": True,
        "testeAdulteracao": True,
        "mensagemOriginal": mensagemOriginal,
        "mensagemRecuperada": mensagemRecuperada
    }


# testar pelo terminal
if __name__ == "__main__":

    print("=== MensagemSegura | Testes de Integridade ===")

    senhaChavePrivada = getpass(
        "\nDigite a senha da chave privada: "
    )

    try:
        resultados = testesIntegridade(
            senhaChavePrivada
        )

        print("\n=== RESULTADO FINAL ===")
        print("Teste da mensagem original: APROVADO")
        print("Teste de detecção de adulteração: APROVADO")
        print("\nTodos os testes foram concluídos com sucesso!")

    except (ValueError, FileNotFoundError, OSError, AssertionError) as erro:
        print("\n[FALHA] Não foi possível concluir os testes.")
        print(f"Detalhes: {erro}")