# MensagemSegura

O **MensagemSegura** é um projeto desenvolvido em Python com o objetivo de demonstrar como proteger mensagens durante uma comunicação.

A aplicação permite criptografar mensagens, criar assinaturas digitais, recuperar mensagens protegidas e verificar se o conteúdo recebido foi alterado.

O projeto foi desenvolvido como uma demonstração prática de conceitos de segurança da informação.

## Funcionalidades

- **Gerenciamento de chaves:** geração e armazenamento de pares de chaves para o remetente e o destinatário.
- **Criptografia de mensagens:** proteção do conteúdo utilizando criptografia híbrida.
- **Assinatura digital:** criação de assinaturas para verificar se uma mensagem corresponde ao conteúdo originalmente assinado.
- **Descriptografia:** recuperação do conteúdo utilizando a chave privada do destinatário.
- **Verificação de integridade:** identificação de alterações nos dados protegidos.
- **Testes de segurança:** demonstração de situações em que uma mensagem original é aceita e situações em que uma mensagem adulterada é rejeitada.

## Tecnologias utilizadas

- Python
- CustomTkinter
- Cryptography

## Algoritmos utilizados

| Algoritmo | Utilização |
|---|---|
| AES-256-GCM | Proteção das mensagens e verificação de alterações. |
| RSA-OAEP com SHA-256 | Proteção da chave utilizada na criptografia da mensagem. |
| RSA-PSS com SHA-256 | Criação e verificação de assinaturas digitais. |
| RSA-3072 | Geração dos pares de chaves. |

## Estrutura do projeto

```text
MensagemSeguraProjeto/
│
├── dados/
│   └── chaves/
│
├── documentacao/
│   └── conceitos.txt
│
├── interface/
│   ├── __init__.py
│   ├── comunicacao.py
│   ├── gerenciadorChaves.py
│   ├── janelaPrincipal.py
│   └── testesSeguranca.py
│
├── seguranca/
│   ├── __init__.py
│   ├── assinatura.py
│   ├── criptografia.py
│   ├── descriptografia.py
│   ├── gerar_chaves.py
│   └── integridade.py
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Requisitos para execução

Antes de iniciar, é necessário possuir:

- Python instalado no computador.
- Pip, ferramenta utilizada para instalar as bibliotecas do Python.

Para conferir se o Python está instalado, abra o terminal e execute:

```bash
py --version
```

## Instalação

**1. Baixe ou clone o projeto.**

Caso utilize Git, execute:

```bash
git clone https://github.com/MattR-Motta/Projeto-Residencia
```

**2. Entre na pasta do projeto.**

```bash
cd Projeto-Residencia
```

**3. Instale as dependências.**

O projeto possui um arquivo chamado `requirements.txt`, que contém as bibliotecas necessárias para executar a aplicação.

Execute:

```bash
py -m pip install -r requerimentos.txt
```

Esse comando instala automaticamente as bibliotecas e as versões especificadas no arquivo.

## Como iniciar a interface

Depois de instalar as dependências, execute o seguinte comando no terminal, estando dentro da pasta principal do projeto:

```bash
py main.py
```

A interface do MensagemSegura será aberta.

## Como utilizar

**1. Gerenciar chaves**

Acesse a opção "Gerenciar chaves" para gerar os pares de chaves do remetente e do destinatário.

As chaves privadas são protegidas por senha e devem ser mantidas em segurança.

**2. Enviar mensagem**

Acesse "Comunicação" e selecione a opção "Enviar mensagem".

Digite o conteúdo desejado e informe a senha da chave privada do remetente.

Clique em "Criptografar e assinar mensagem".

A aplicação produzirá os dados protegidos e a assinatura digital em um pacote que pode ser copiado para compartilhamento.

**3. Receber mensagem**

Na mesma página, selecione "Receber mensagem".

Insira os dados recebidos e informe a senha da chave privada do destinatário.

Clique em "Descriptografar e verificar assinatura".

A aplicação apresentará a mensagem recuperada e o resultado da verificação da assinatura.

**4. Testes de segurança**

Acesse "Testes de segurança" para executar demonstrações de integridade e autenticidade.

Os testes verificam o comportamento do sistema diante de mensagens originais e de mensagens modificadas.

## Cuidados com as chaves

As chaves privadas são informações importantes e não devem ser compartilhadas.

Não envie arquivos de chave privada para o GitHub ou para outras pessoas.

As chaves públicas podem ser compartilhadas, mas é necessário confirmar sua origem antes de utilizá-las para confiar em uma comunicação.

## Limitações do projeto

O MensagemSegura é um protótipo acadêmico desenvolvido para demonstrar mecanismos de proteção de mensagens.

A aplicação não possui comunicação automática entre computadores, emissão de certificados digitais ou implementação de uma estrutura PKI.

A confirmação da identidade real do remetente depende de uma forma confiável de associar sua identidade à chave pública utilizada na verificação.

Portanto, a solução demonstra conceitos importantes de segurança, mas não substitui um sistema completo de comunicação segura.

## Objetivo acadêmico

Este projeto tem como finalidade aplicar conhecimentos de segurança da informação por meio da implementação e demonstração de mecanismos de criptografia, integridade e assinatura digital.