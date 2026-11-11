import base64
from getpass import getpass
from pathlib import Path
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def obterPastaChaves():
    return (Path(__file__).resolve().parent.parent/ "dados"/ "chaves")

def gerarParChavesAssinatura(senhaChavePrivada, pastaDestino=None):
    # Gera um par de chaves RSA exclusivo para assinatura digital a chave privada é protegida por senha e a chave pública pode ser compartilhada para verificar assinaturas.
    if not isinstance(senhaChavePrivada, str) or len(senhaChavePrivada) < 8:
        raise ValueError("A senha deve possuir pelo menos 8 caracteres.")
    if pastaDestino is None:
        pastaDestino = obterPastaChaves()
    else:
        pastaDestino = Path(pastaDestino)

    pastaDestino.mkdir(parents=True, exist_ok=True)
    caminhoChavePrivada = pastaDestino / "remetente_private.pem"
    caminhoChavePublica = pastaDestino / "remetente_public.pem"

    if caminhoChavePrivada.exists() or caminhoChavePublica.exists():
        raise FileExistsError("Já existem chaves de assinatura nesta pasta. ")

    # gera a chave privada RSA de 3072 bits
    chavePrivada = rsa.generate_private_key(public_exponent=65537,key_size=3072)
    chavePublica = chavePrivada.public_key()

    # protege a chave privada com a senha informada
    chavePrivadaPem = chavePrivada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            senhaChavePrivada.encode("utf-8")
        )
    )

    # exporta a chave pública
    chavePublicaPem = chavePublica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    caminhoChavePrivada.write_bytes(chavePrivadaPem)
    caminhoChavePublica.write_bytes(chavePublicaPem)
    return caminhoChavePrivada, caminhoChavePublica


def assinarMensagem(mensagemOriginal,senhaChavePrivada,caminhoChavePrivada=None):
    # gera uma assinatura digital RSA-PSS para uma mensagem e etorna a assinatura codificada em Base64.

    if not isinstance(mensagemOriginal, str) or not mensagemOriginal:
        raise ValueError("A mensagem não pode estar vazia.")

    if not isinstance(senhaChavePrivada, str) or not senhaChavePrivada:
        raise ValueError("A senha da chave privada não foi informada.")

    if caminhoChavePrivada is None:
        caminhoChavePrivada = (
            obterPastaChaves() / "remetente_private.pem"
        )
    else:
        caminhoChavePrivada = Path(caminhoChavePrivada)

    if not caminhoChavePrivada.is_file():
        raise FileNotFoundError("Chave privada do remetente não encontrada.")

    # Carrega a chave privada protegida por senha
    try:
        chavePrivada = serialization.load_pem_private_key(
            caminhoChavePrivada.read_bytes(),
            password=senhaChavePrivada.encode("utf-8")
        )
    except (ValueError, TypeError) as erro:
        raise ValueError(
            "Não foi possível abrir a chave privada. Verifique a senha."
        ) from erro

    if not isinstance(chavePrivada, rsa.RSAPrivateKey):
        raise ValueError("O arquivo não contém uma chave privada RSA.")

    # assina os bytes da mensagem com RSA-PSS e SHA-256
    assinatura = chavePrivada.sign(
        mensagemOriginal.encode("utf-8"),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return base64.b64encode(assinatura).decode("utf-8")


def verificarAssinatura(mensagemOriginal,assinaturaBase64,caminhoChavePublica=None):
    # verifica uma assinatura digital RSA-PSS retorna True quando a assinatura é válida e False quando é inválida
    if not isinstance(mensagemOriginal, str) or not mensagemOriginal:
        raise ValueError("A mensagem não pode estar vazia.")

    if not isinstance(assinaturaBase64, str) or not assinaturaBase64:
        raise ValueError("A assinatura não foi informada.")

    if caminhoChavePublica is None:
        caminhoChavePublica = (
            obterPastaChaves() / "remetente_public.pem"
        )
    else:
        caminhoChavePublica = Path(caminhoChavePublica)

    if not caminhoChavePublica.is_file():
        raise FileNotFoundError("Chave pública do remetente não encontrada.")
    chavePublica = serialization.load_pem_public_key(caminhoChavePublica.read_bytes())
    if not isinstance(chavePublica, rsa.RSAPublicKey):
        raise ValueError("O arquivo não contém uma chave pública RSA.")
    # recupera os bytes da assinatura
    try:
        assinatura = base64.b64decode(assinaturaBase64,validate=True)
    except (ValueError, TypeError) as erro:
        raise ValueError("A assinatura possui codificação inválida.") from erro

    # verifica se a assinatura corresponde a mensagem
    try:
        chavePublica.verify(
            assinatura,
            mensagemOriginal.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True

    except InvalidSignature:
        return False

# testa
if __name__ == "__main__":

    print("=== MensagemSegura | Assinatura Digital RSA-PSS ===")

    senhaChavePrivada = getpass(
        "\nCrie uma senha para a chave privada do remetente: "
    )

    confirmacaoSenha = getpass(
        "Confirme a senha: "
    )

    if senhaChavePrivada != confirmacaoSenha:
        print("\nErro: as senhas não coincidem.")

    else:
        try:
            caminhoChavePrivada = obterPastaChaves() / "remetente_private.pem"
            caminhoChavePublica = obterPastaChaves() / "remetente_public.pem"

            if not caminhoChavePrivada.exists() and not caminhoChavePublica.exists():
                gerarParChavesAssinatura(senhaChavePrivada)
                print("\nPar de chaves de assinatura gerado com sucesso!")

            elif not caminhoChavePrivada.exists() or not caminhoChavePublica.exists():
                raise FileNotFoundError(
                    "O par de chaves está incompleto. "
                    "Verifique os arquivos antes de continuar."
                )

            else:
                print("\nPar de chaves de assinatura já existente.")

            mensagemOriginal = input(
                "\nDigite a mensagem que deseja assinar: "
            )

            # Gera a assinatura digital
            assinaturaBase64 = assinarMensagem(
                mensagemOriginal,
                senhaChavePrivada
            )

            print("\nAssinatura digital gerada com sucesso!")

            # Verifica a assinatura original
            resultadoOriginal = verificarAssinatura(
                mensagemOriginal,
                assinaturaBase64
            )

            print(
                "\nVerificação da mensagem original:",
                "VÁLIDA" if resultadoOriginal else "INVÁLIDA"
            )

            # Simula a alteração da mensagem
            mensagemAdulterada = mensagemOriginal + " (adulterada)"

            resultadoAdulterado = verificarAssinatura(
                mensagemAdulterada,
                assinaturaBase64
            )

            print(
                "Verificação da mensagem adulterada:",
                "VÁLIDA" if resultadoAdulterado else "INVÁLIDA"
            )

            if resultadoOriginal and not resultadoAdulterado:
                print("\nTodos os testes de assinatura foram aprovados!")
            else:
                print("\nFalha em um ou mais testes de assinatura.")

        except (ValueError, FileNotFoundError, FileExistsError, OSError) as erro:
            print(f"\nNão foi possível concluir a operação: {erro}")