from pathlib import Path
from typing import Optional, Union
from getpass import getpass
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def gerarParChaves(senha: str,pastaDestino: Optional[Union[str, Path]] = None):
    # Gera um par de chaves RSA e salva os arquivos em formato PEM a chave privada é protegida por senh a a chave pública pode ser compartilhada com o remetente.
    # verifica se a senha foi informada corretamente
    if not isinstance(senha, str) or len(senha) < 8:
        raise ValueError("A senha deve possuir pelo menos 8 caracteres.")

    if pastaDestino is None:
        pastaDestino = (Path(__file__).resolve().parent.parent / "dados" / "chaves")
    else:
        pastaDestino = Path(pastaDestino)

    # cria a pasta caso ela ainda não exista
    pastaDestino.mkdir(parents=True, exist_ok=True)
    caminhoPrivada = pastaDestino / "destinatario_private.pem"
    caminhoPublica = pastaDestino / "destinatario_public.pem"

    # evita ter q substituir chaves que ja existem
    if caminhoPrivada.exists() or caminhoPublica.exists():
        raise FileExistsError("Já existem arquivos de chaves nesta pasta. ")

    # gera a chave privada RSA
    chavePrivada = rsa.generate_private_key(public_exponent=65537,key_size=3072)

    # consegu a chave pública correspondente
    chavePublica = chavePrivada.public_key()

    # converte a chave privada para o formato PEM
    privadaPem = chavePrivada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            senha.encode("utf-8")
        )
    )

    # converte a chave pública para o formato PEM
    publicaPem = chavePublica.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

    # salva os arquivos no computador na pasta das chves
    caminhoPrivada.write_bytes(privadaPem)
    caminhoPublica.write_bytes(publicaPem)

    return caminhoPrivada, caminhoPublica


# as senhas não serão visiveis no terminal não ta
if __name__ == "__main__":
    print("MensagemSegura | Gerador de Chaves RSA")

    senha = getpass("Crie uma senha para proteger a chave privada: ")
    confirmacao = getpass("Confirme a senha: ")

    if senha != confirmacao:
        print("\nErro: as senhas não coincidem.")
    else:
        try:
            arquivoPrivado, arquivoPublico = gerarParChaves(senha)
            print("\nPar de chaves RSA gerado com sucesso!")
            print(f"\nChave privada: {arquivoPrivado}")
            print(f"Chave pública: {arquivoPublico}")
        except (ValueError, FileExistsError, OSError) as erro:
            print(f"\nNão foi possível gerar as chaves: {erro}")