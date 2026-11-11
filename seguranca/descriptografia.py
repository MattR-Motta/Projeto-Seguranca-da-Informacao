import base64
from pathlib import Path
from getpass import getpass
from cryptography.exceptions import InvalidTag, InvalidKey
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def descriptografarMensagem(dadosCriptografados,senhaChavePrivada,caminhoChavePrivada=None):

    if not isinstance(dadosCriptografados, dict):
        raise ValueError("Os dados criptografados devem estar em formato de dicionário.")

    if not isinstance(senhaChavePrivada, str) or not senhaChavePrivada:
        raise ValueError("A senha da chave privada não foi informada.")
    
    camposObrigatorios = [
        "algoritmoMensagem",
        "algoritmoChave",
        "nonce",
        "chaveCriptografada",
        "mensagemCriptografada"
    ]

    for campo in camposObrigatorios:
        if campo not in dadosCriptografados:
            raise ValueError(f"Campo obrigatório ausente: {campo}")

    # verifica os algoritmos utilizados
    if dadosCriptografados["algoritmoMensagem"] != "AES-256-GCM":
        raise ValueError("Algoritmo de mensagem não reconhecido.")

    if dadosCriptografados["algoritmoChave"] != "RSA-OAEP-SHA256":
        raise ValueError("Algoritmo de proteção da chave não reconhecido.")

    # define o caminho da chave privada
    if caminhoChavePrivada is None:
        caminhoChavePrivada = (Path(__file__).resolve().parent.parent/ "dados"/ "chaves"/ "destinatario_private.pem")
    else:
        caminhoChavePrivada = Path(caminhoChavePrivada)

    # verifica se o arquivo da chave privada existe
    if not caminhoChavePrivada.is_file():
        raise FileNotFoundError("Arquivo da chave privada não encontrado.")
    # carrega a chave privada utilizando a senha
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
        raise ValueError("O arquivo informado não contém uma chave privada RSA.")
    try:
        # recupera os dados binários a partir do Base64
        nonce = base64.b64decode(dadosCriptografados["nonce"],validate=True)
        chaveCifrada = base64.b64decode(dadosCriptografados["chaveCriptografada"],validate=True)
        mensagemCifrada = base64.b64decode(dadosCriptografados["mensagemCriptografada"],validate=True)

    except (ValueError, TypeError) as erro:
        raise ValueError("Os dados recebidos possuem codificação inválida.") from erro

    # verifica o tamanho do nonce
    if len(nonce) != 12:
        raise ValueError("O nonce informado possui tamanho inválido.")

    # recupera a chave AES utilizando RSA-OAEP
    try:
        chaveTemporaria = chavePrivada.decrypt(
            chaveCifrada,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except ValueError as erro:
        raise ValueError("Não foi possível recuperar a chave AES. Verifique se a chave privada corresponde à chave pública utilizada."
        ) from erro

    # descriptografa a mensagem e verifica a autenticidade e integridade
    try:
        algoritmoAES = AESGCM(chaveTemporaria)

        mensagemOriginal = algoritmoAES.decrypt(nonce,mensagemCifrada,None)

    except InvalidTag as erro:
        raise ValueError("Falha na autenticação! A mensagem pode ter sido adulterada ou os dados utilizados podem estar incorretos.") from erro
    # converte os bytes recuperados para texto
    try:
        mensagemOriginal = mensagemOriginal.decode("utf-8")
    except UnicodeDecodeError as erro:
        raise ValueError("Não foi possível interpretar a mensagem recuperada.") from erro

    return mensagemOriginal