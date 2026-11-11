import base64
import os
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def criptografarMensagem(mensagemOriginal, caminhoChavePublica=None):
    # criptografa uma mensagem utilizando AES-256-GCM e protege a chave AES utilizando RSA-OAEP e retorna um dicionário contendo os dados necessários para que o destinatário possa descriptografar a mensagem.
    

    if not isinstance(mensagemOriginal, str) or not mensagemOriginal.strip():
        raise ValueError("A mensagem não pode estar vazia.")

    if caminhoChavePublica is None:
        caminhoChavePublica = (Path(__file__).resolve().parent.parent/ "dados"/ "chaves"/ "destinatario_public.pem")
    else:
        caminhoChavePublica = Path(caminhoChavePublica)

    # verifica se o arquivo da chave pública existe
    if not caminhoChavePublica.is_file():
        raise FileNotFoundError("Arquivo da chave pública não encontrado.")

    # carrega a chave pública
    chavePublica = serialization.load_pem_public_key(
        caminhoChavePublica.read_bytes()
    )

    # verifica se a chave carregada é RSA
    if not isinstance(chavePublica, rsa.RSAPublicKey):
        raise ValueError("O arquivo informado não contém uma chave pública RSA.")

    # gera uma chave AES aleatória de 256 bits
    chaveTemporaria = AESGCM.generate_key(bit_length=256)
    # gera um nonce aleatório de 12 bytes
    nonce = os.urandom(12)
    # converte a mensagem para bytes
    mensagemBytes = mensagemOriginal.encode("utf-8")
    # criptografa a mensagem utilizando AES-GCM
    algoritmoAES = AESGCM(chaveTemporaria)
    mensagemCifrada = algoritmoAES.encrypt(
        nonce,
        mensagemBytes,
        None
    )

    # protege a chave AES utilizando RSA-OAEP
    chaveCifrada = chavePublica.encrypt(
        chaveTemporaria,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None)
    )

    # organizacao dos daods
    dadosCriptografados = {
        "algoritmoMensagem": "AES-256-GCM",
        "algoritmoChave": "RSA-OAEP-SHA256",
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "chaveCriptografada": base64.b64encode(chaveCifrada).decode("utf-8"),
        "mensagemCriptografada": base64.b64encode(mensagemCifrada).decode("utf-8")
    }

    return dadosCriptografados


# pra testar a criptografia diretamente pelo terminal
if __name__ == "__main__":

    print("=== MensgaemSegura | Criptografia ===")

    mensagemOriginal = input("\nDigite a mensagem que deseja criptografar: ")

    try:
        dadosCriptografados = criptografarMensagem(mensagemOriginal)

        print("\nMensagem criptografada com sucesso!")
        print("\n=== DADOS PARA ENVIO ===")

        for nomeCampo, valorCampo in dadosCriptografados.items():
            print(f"\n{nomeCampo}:")
            print(valorCampo)

    except (ValueError, FileNotFoundError, OSError) as erro:
        print(f"\nErro ao criptografar: {erro}")