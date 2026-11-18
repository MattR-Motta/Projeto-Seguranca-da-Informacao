import sqlite3
import customtkinter as ctk
from tkinter import messagebox

from autenticacao.servico import autenticarUsuario, cadastrarUsuario


class Autenticacao(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent", corner_radius=0)

        self.corCartao = "#1E2433"
        self.corPrimaria = "#5146D8"
        self.corTexto = "#FFFFFF"
        self.corTextoSecundario = "#A7AEC0"
        self.usuarioAutenticado = None

        self.criarInterface()

    def criarInterface(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        titulo = ctk.CTkLabel(
            self,
            text="Cadastro e autenticação segura",
            font=("Arial", 26, "bold"),
            text_color=self.corTexto,
        )
        titulo.grid(row=0, column=0, sticky="w", padx=25, pady=(25, 8))

        descricao = ctk.CTkLabel(
            self,
            text=(
                "Cadastre uma conta e entre utilizando senhas protegidas "
                "com Argon2id."
            ),
            font=("Arial", 13),
            text_color=self.corTextoSecundario,
        )
        descricao.grid(row=1, column=0, sticky="w", padx=25, pady=(0, 18))

        self.abas = ctk.CTkTabview(
            self,
            fg_color=self.corCartao,
            segmented_button_selected_color=self.corPrimaria,
            segmented_button_selected_hover_color="#4035B5",
        )
        self.abas.grid(row=2, column=0, sticky="nsew", padx=25, pady=(0, 15))

        self.abaCadastro = self.abas.add("Criar conta")
        self.abaLogin = self.abas.add("Entrar")

        self.criarAbaCadastro()
        self.criarAbaLogin()

        self.statusSessao = ctk.CTkLabel(
            self,
            text="Nenhum usuário autenticado nesta sessão.",
            font=("Arial", 12),
            text_color=self.corTextoSecundario,
        )
        self.statusSessao.grid(row=3, column=0, sticky="w", padx=25, pady=(0, 20))

    def criarAbaCadastro(self):
        self.abaCadastro.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.abaCadastro,
            text="Nome de usuário",
            text_color=self.corTexto,
            font=("Arial", 13),
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(22, 5))

        self.cadastroUsuario = ctk.CTkEntry(
            self.abaCadastro,
            placeholder_text="Escolha um nome de usuário",
            height=40,
        )
        self.cadastroUsuario.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

        ctk.CTkLabel(
            self.abaCadastro,
            text="Senha (mínimo de 8 caracteres)",
            text_color=self.corTexto,
            font=("Arial", 13),
        ).grid(row=2, column=0, sticky="w", padx=20, pady=(5, 5))

        self.cadastroSenha = ctk.CTkEntry(
            self.abaCadastro,
            placeholder_text="Crie uma senha",
            show="*",
            height=40,
        )
        self.cadastroSenha.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 12))

        ctk.CTkLabel(
            self.abaCadastro,
            text="Confirme a senha",
            text_color=self.corTexto,
            font=("Arial", 13),
        ).grid(row=4, column=0, sticky="w", padx=20, pady=(5, 5))

        self.cadastroConfirmacao = ctk.CTkEntry(
            self.abaCadastro,
            placeholder_text="Digite a senha novamente",
            show="*",
            height=40,
        )
        self.cadastroConfirmacao.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 15))

        ctk.CTkButton(
            self.abaCadastro,
            text="Cadastrar usuário",
            height=42,
            fg_color=self.corPrimaria,
            hover_color="#4035B5",
            command=self.cadastrar,
        ).grid(row=6, column=0, sticky="w", padx=20, pady=(0, 20))

    def criarAbaLogin(self):
        self.abaLogin.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.abaLogin,
            text="Nome de usuário",
            text_color=self.corTexto,
            font=("Arial", 13),
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(22, 5))

        self.loginUsuario = ctk.CTkEntry(
            self.abaLogin,
            placeholder_text="Informe seu nome de usuário",
            height=40,
        )
        self.loginUsuario.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

        ctk.CTkLabel(
            self.abaLogin,
            text="Senha",
            text_color=self.corTexto,
            font=("Arial", 13),
        ).grid(row=2, column=0, sticky="w", padx=20, pady=(5, 5))

        self.loginSenha = ctk.CTkEntry(
            self.abaLogin,
            placeholder_text="Informe sua senha",
            show="*",
            height=40,
        )
        self.loginSenha.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 15))

        ctk.CTkButton(
            self.abaLogin,
            text="Entrar",
            height=42,
            fg_color=self.corPrimaria,
            hover_color="#4035B5",
            command=self.entrar,
        ).grid(row=4, column=0, sticky="w", padx=20, pady=(0, 20))

    def cadastrar(self):
        nomeUsuario = self.cadastroUsuario.get().strip()
        senha = self.cadastroSenha.get()
        confirmacaoSenha = self.cadastroConfirmacao.get()

        if senha != confirmacaoSenha:
            messagebox.showwarning(
                "Confirmação inválida",
                "A confirmação não corresponde à senha informada.",
            )
            return

        try:
            cadastrarUsuario(nomeUsuario, senha)
            self.cadastroSenha.delete(0, "end")
            self.cadastroConfirmacao.delete(0, "end")
            self.loginUsuario.delete(0, "end")
            self.loginUsuario.insert(0, nomeUsuario)
            self.abas.set("Entrar")
            messagebox.showinfo(
                "Cadastro concluído",
                "Usuário cadastrado. A senha foi armazenada somente como hash Argon2id.",
            )
        except ValueError as erro:
            messagebox.showwarning("Não foi possível cadastrar", str(erro))
        except (OSError, sqlite3.Error) as erro:
            messagebox.showerror("Erro de armazenamento", str(erro))

    def entrar(self):
        nomeUsuario = self.loginUsuario.get().strip()
        senha = self.loginSenha.get()

        if autenticarUsuario(nomeUsuario, senha):
            self.usuarioAutenticado = nomeUsuario
            self.loginSenha.delete(0, "end")
            self.statusSessao.configure(
                text=f"Sessão autenticada: {nomeUsuario}",
                text_color="#55D68B",
            )
            messagebox.showinfo(
                "Autenticação concluída",
                f"Bem-vindo, {nomeUsuario}! As credenciais foram verificadas.",
            )
        else:
            self.usuarioAutenticado = None
            self.statusSessao.configure(
                text="Falha na autenticação. Verifique usuário e senha.",
                text_color="#E57373",
            )
            messagebox.showwarning(
                "Acesso negado",
                "Nome de usuário ou senha incorretos.",
            )