# MensagemSegura

O **MensagemSegura** é uma aplicação acadêmica desenvolvida em Python para demonstrar mecanismos de segurança da informação aplicados à proteção de mensagens e à autenticação de usuários.

O projeto reúne criptografia híbrida, assinatura digital, verificação de integridade e cadastro/login com armazenamento seguro de senhas.

## Funcionalidades

- **Gerenciamento de chaves:** geração e armazenamento de pares de chaves do remetente e do destinatário.
- **Criptografia de mensagens:** proteção do conteúdo utilizando criptografia híbrida.
- **Assinatura digital:** criação e verificação de assinaturas para validar a autenticidade e detectar alterações.
- **Descriptografia:** recuperação do conteúdo utilizando a chave privada do destinatário.
- **Verificação de integridade:** identificação de alterações nos dados protegidos.
- **Cadastro e login:** criação de contas e autenticação de usuários com Argon2id.
- **Testes de segurança:** testes de criptografia, integridade, assinatura e autenticação.

## Tecnologias e algoritmos

| Tecnologia/algoritmo | Utilização |
|---|---|
| Python | Linguagem de desenvolvimento. |
| CustomTkinter | Interface gráfica. |
| Cryptography | Operações criptográficas e gerenciamento de chaves. |
| SQLite | Persistência local dos registros de usuários. |
| Argon2id (`argon2-cffi`) | Derivação e verificação de hashes de senhas. |
| AES-256-GCM | Proteção das mensagens e verificação de alterações. |
| RSA-OAEP com SHA-256 | Proteção da chave utilizada na criptografia da mensagem. |
| RSA-PSS com SHA-256 | Criação e verificação de assinaturas digitais. |
| RSA-3072 | Geração dos pares de chaves. |

## Estrutura do projeto

```text
Projeto-Seguranca-da-Informacao/
│
├── autenticacao/
│   ├── __init__.py
│   ├── armazenamento.py
│   └── servico.py
│
├── dados/
│   ├── chaves/
│   └── usuarios.db              (criado automaticamente na primeira conta)
│
├── documentacao/
│   ├── conceitos.txt
│   ├── fluxo_autenticacao.md
│   └── evidencia_registro_protegido.txt
│
├── interface/
│   ├── __init__.py
│   ├── autenticacao.py
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
│   ├── gerarChaves.py
│   └── integridade.py
│
├── testes/
│   ├── __init__.py
│   ├── demonstrarRegistroProtegido.py
│   └── test_autenticacao.py
│
├── .gitignore
├── main.py
├── README.md
└── requerimentos.txt
```

## Requisitos para execução

- Python 3.10 ou superior.
- Pip, ferramenta utilizada para instalar as bibliotecas Python.

Para conferir a instalação:

```bash
py --version
```

## Instalação

1. Baixe ou clone o projeto.
2. Abra o terminal na pasta `Projeto-Seguranca-da-Informacao`.
3. Instale as dependências:

```bash
py -m pip install -r requerimentos.txt
```

## Como iniciar a interface

Execute na pasta principal do projeto:

```bash
py main.py
```

A interface do MensagemSegura será aberta.

## Como utilizar

### 1. Cadastro e autenticação

Acesse **Autenticação** no menu lateral.

- Na aba **Criar conta**, informe um nome de usuário, uma senha com pelo menos 8 caracteres e a confirmação.
- Após o cadastro, acesse a aba **Entrar** e informe as credenciais.
- O sistema valida a senha usando o método `PasswordHasher.verify()` da biblioteca Argon2.

O banco SQLite `dados/usuarios.db` é criado automaticamente. A senha original não é gravada: somente a representação codificada do hash Argon2id é armazenada.

### 2. Gerenciar chaves

Acesse **Gerenciar chaves** para gerar os pares de chaves do remetente e do destinatário. As chaves privadas são protegidas por senha e devem ser mantidas em segurança.

### 3. Enviar mensagem

Acesse **Comunicação** e selecione a opção de envio. Digite o conteúdo e informe a senha da chave privada do remetente. Clique em **Criptografar e assinar mensagem**. A aplicação produzirá os dados protegidos e a assinatura digital em um pacote que pode ser copiado para compartilhamento.

### 4. Receber mensagem

Na mesma página, selecione a opção de recebimento. Insira os dados recebidos e informe a senha da chave privada do destinatário. Clique em **Descriptografar e verificar assinatura**.

### 5. Testes

Acesse **Testes de segurança** para executar as demonstrações de integridade e autenticidade. Os testes automatizados da autenticação são executados conforme a seção abaixo.

## Testes da Etapa 2

Na pasta principal, execute:

```bash
py -m unittest discover -s testes -v
```

Os testes automatizados verificam:

- Login com senha correta.
- Rejeição de senha incorreta.
- Rejeição de usuário inexistente.
- Armazenamento do hash, sem armazenar a senha em texto puro.
- Geração de hashes diferentes para a mesma senha em contas distintas (salt individual).
- Rejeição de nome de usuário duplicado.
- Rejeição de senha abaixo do tamanho mínimo.

Para gerar uma demonstração de registro protegido no terminal:

```bash
py -m testes.demonstrarRegistroProtegido
```

O script utiliza um banco temporário, exibe o hash Argon2id e remove o banco ao terminar. Ele não altera o banco de usuários da aplicação.

## Por que não utilizar SHA-256 isoladamente para senhas?

SHA-256 é uma função de hash criptográfica geral, projetada para ser rápida. Essa característica é útil para integridade, mas é desfavorável ao armazenamento de senhas: um atacante que obtenha os hashes pode testar um grande número de tentativas rapidamente, inclusive com hardware paralelo.

Além disso, o uso isolado de SHA-256 não gera automaticamente um salt individual nem oferece parâmetros de custo ajustáveis para tornar cada tentativa mais cara.

Argon2id foi projetado para derivação de senhas. Ele utiliza memória e tempo configuráveis e gera um salt aleatório para cada hash. Isso dificulta ataques de tentativa em massa e impede que senhas iguais produzam necessariamente o mesmo hash.

## Configuração do Argon2id

A implementação define explicitamente os seguintes parâmetros:

| Parâmetro | Valor |
|---|---:|
| Variante | Argon2id |
| `time_cost` | 3 |
| `memory_cost` | 65536 KiB (64 MiB) |
| `parallelism` | 4 |
| `hash_len` | 32 bytes |
| `salt_len` | 16 bytes |

A biblioteca gera o salt aleatoriamente e inclui salt e parâmetros na representação codificada do hash (formato PHC). Por isso, o projeto não precisa armazenar o salt em uma coluna separada.

A comparação de senha não é feita com `==` entre hashes. O sistema utiliza `_hasher.verify(hashArmazenado, senhaInformada)`, fornecido pela biblioteca Argon2.

## Cuidados com os dados

- Não compartilhe chaves privadas.
- Não versionar o banco `dados/usuarios.db`, pois ele contém registros de contas e hashes.
- O banco é local e não possui criptografia de arquivo; mantenha o computador e os arquivos de dados protegidos.
- A autenticação desta etapa demonstra cadastro e validação de credenciais na aplicação. Ela não implementa controle de autorização por perfil para cada operação do sistema.

## Limitações do projeto

O MensagemSegura é um protótipo acadêmico. A aplicação não possui comunicação automática entre computadores, emissão de certificados digitais ou implementação de uma estrutura PKI.

O banco de usuários é SQLite local. Para uso em produção, seriam necessários controles adicionais, como proteção do ambiente, política de recuperação de conta, limitação de tentativas, gestão de sessão e revisão de segurança da aplicação.

## Objetivo acadêmico

O projeto aplica conceitos de segurança da informação por meio da implementação e demonstração de criptografia, integridade, assinatura digital e autenticação segura de usuários.