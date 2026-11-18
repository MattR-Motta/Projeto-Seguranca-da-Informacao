# Etapa 2 — Hash e autenticação segura

## 1. Objetivo

Permitir o cadastro e o login de usuários sem armazenar senhas em texto puro.

## 2. Componentes implementados

- `autenticacao/servico.py`: valida os dados, gera hashes Argon2id, cadastra usuários e autentica credenciais.
- `autenticacao/armazenamento.py`: cria e acessa a tabela SQLite de usuários.
- `interface/autenticacao.py`: apresenta as abas de cadastro e login.
- `testes/test_autenticacao.py`: contém testes automatizados.
- `testes/demonstrarRegistroProtegido.py`: demonstra o formato do registro salvo sem utilizar o banco real da aplicação.

## 3. Fluxo de cadastro

1. O usuário informa nome, senha e confirmação na interface.
2. A aplicação valida os campos e exige senha com pelo menos 8 caracteres.
3. `PasswordHasher.hash()` gera um hash Argon2id com salt aleatório.
4. O SQLite armazena o nome de usuário, o hash codificado e a data de criação.
5. A senha original não é inserida no banco.

## 4. Fluxo de login

1. O usuário informa nome e senha.
2. O serviço localiza o hash associado ao nome de usuário.
3. `PasswordHasher.verify()` compara a senha informada com o hash armazenado.
4. Se a verificação for válida, o login é aceito; caso contrário, o acesso é negado.

O serviço também rejeita usuários inexistentes e hashes inválidos. A consulta SQL utiliza parâmetros, evitando a concatenação direta de dados do usuário na instrução.

## 5. Argon2id e salt

O projeto utiliza Argon2id com `time_cost=3`, `memory_cost=65536`, `parallelism=4`, `hash_len=32` e `salt_len=16`.

O salt é gerado pela biblioteca para cada senha. O hash codificado contém a variante, os parâmetros, o salt e o resultado derivado. Portanto, o salt não precisa de uma coluna separada no banco.

## 6. Por que SHA-256 isolado não é adequado?

SHA-256 é rápido e não foi projetado especificamente para armazenamento de senhas. Sua velocidade permite que muitas tentativas sejam testadas rapidamente. Quando utilizado isoladamente, também não inclui automaticamente salt individual nem custo configurável.

Argon2id foi projetado para derivação de senhas e permite configurar custo de memória e tempo. O salt individual reduz a possibilidade de hashes iguais para senhas iguais e dificulta o uso de tabelas pré-computadas.

SHA-256 continua sendo utilizado no projeto em outros contextos criptográficos, como RSA-OAEP e RSA-PSS, mas isso não significa que seja apropriado como hash isolado de senha.

## 7. Testes

Execute na pasta principal:

```bash
py -m unittest discover -s testes -v
```

Os casos verificam login correto, senha incorreta, usuário inexistente, armazenamento do hash em vez da senha, salts distintos, usuário duplicado e senha curta.

## 8. Evidência de armazenamento protegido

Execute:

```bash
py -m testes.demonstrarRegistroProtegido
```

O script cria um banco temporário, cadastra uma conta demonstrativa e exibe a representação Argon2id armazenada. A senha demonstrativa não é exibida e o banco temporário é removido ao final.

## 9. Limites

O banco SQLite é local e não criptografa o arquivo inteiro. A entrega demonstra hash de senha e autenticação, mas não implementa ainda controle de autorização para todas as funcionalidades, recuperação de senha, limitação de tentativas ou gerenciamento avançado de sessões.