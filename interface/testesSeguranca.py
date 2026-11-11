import base64
import copy
import customtkinter as ctk
from tkinter import messagebox
from seguranca.criptografia import criptografarMensagem
from seguranca.descriptografia import descriptografarMensagem
from seguranca.assinatura import assinarMensagem, verificarAssinatura

class TestesSeguranca(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#10131C",
            corner_radius=0
        )

        self.corCartao = "#1E2433"
        self.corPrimaria = "#5146D8"
        self.corTexto = "#FFFFFF"
        self.corTextoSecundario = "#A7AEC0"
        self.corSucesso = "#2ECC71"
        self.corErro = "#E74C3C"

        self.criarInterface()

    def criarInterface(self):
        """Monta a página de testes de segurança."""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        titulo = ctk.CTkLabel(
            self,
            text="Testes de segurança",
            font=("Arial", 26, "bold"),
            text_color=self.corTexto
        )

        titulo.grid(
            row=0,
            column=0,
            sticky="w",
            padx=25,
            pady=(20, 5)
        )

        descricao = ctk.CTkLabel(
            self,
            text="Execute testes para verificar a integridade e a autenticidade das mensagens.",
            font=("Arial", 13),
            text_color=self.corTextoSecundario
        )

        descricao.grid(
            row=1,
            column=0,
            sticky="w",
            padx=25,
            pady=(0, 15)
        )

        self.areaTestes = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.areaTestes.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 20)
        )

        self.areaTestes.grid_columnconfigure(0, weight=1)

        self.criarTesteIntegridade()
        self.criarTesteAssinatura()
        self.criarAreaResultados()

    def criarTesteIntegridade(self):
        """Cria a seção de testes de integridade."""

        cartao = ctk.CTkFrame(
            self.areaTestes,
            fg_color=self.corCartao,
            corner_radius=12
        )

        cartao.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=10
        )

        cartao.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            cartao,
            text="1. Teste de integridade",
            font=("Arial", 17, "bold"),
            text_color=self.corTexto
        )

        titulo.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 5)
        )

        descricao = ctk.CTkLabel(
            cartao,
            text=(
                "Verifica se o AES-256-GCM consegue detectar alterações "
                "nos dados criptografados."
            ),
            font=("Arial", 12),
            text_color=self.corTextoSecundario,
            wraplength=750,
            justify="left"
        )

        descricao.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 12)
        )

        tituloSenha = ctk.CTkLabel(
            cartao,
            text="Senha da chave privada do destinatário:",
            font=("Arial", 12),
            text_color=self.corTexto
        )

        tituloSenha.grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.senhaIntegridade = ctk.CTkEntry(
            cartao,
            placeholder_text="Digite a senha da chave do destinatário",
            show="*",
            height=38,
            width=400
        )

        self.senhaIntegridade.grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 12)
        )

        botaoExecutar = ctk.CTkButton(
            cartao,
            text="Executar teste de integridade",
            height=40,
            fg_color=self.corPrimaria,
            hover_color="#4035B5",
            command=self.testarIntegridade
        )

        botaoExecutar.grid(
            row=4,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 18)
        )

    def criarTesteAssinatura(self):
        """Cria a seção de testes de assinatura digital."""

        cartao = ctk.CTkFrame(
            self.areaTestes,
            fg_color=self.corCartao,
            corner_radius=12
        )

        cartao.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=10
        )

        cartao.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            cartao,
            text="2. Teste de autenticidade",
            font=("Arial", 17, "bold"),
            text_color=self.corTexto
        )

        titulo.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 5)
        )

        descricao = ctk.CTkLabel(
            cartao,
            text=(
                "Verifica se o RSA-PSS identifica uma mensagem alterada "
                "após a geração da assinatura digital."
            ),
            font=("Arial", 12),
            text_color=self.corTextoSecundario,
            wraplength=750,
            justify="left"
        )

        descricao.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 12)
        )

        tituloSenha = ctk.CTkLabel(
            cartao,
            text="Senha da chave privada do remetente:",
            font=("Arial", 12),
            text_color=self.corTexto
        )

        tituloSenha.grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.senhaAssinatura = ctk.CTkEntry(
            cartao,
            placeholder_text="Digite a senha da chave de assinatura",
            show="*",
            height=38,
            width=400
        )

        self.senhaAssinatura.grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 12)
        )

        botaoExecutar = ctk.CTkButton(
            cartao,
            text="Executar teste de assinatura",
            height=40,
            fg_color=self.corPrimaria,
            hover_color="#4035B5",
            command=self.testarAssinatura
        )

        botaoExecutar.grid(
            row=4,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 18)
        )

    def criarAreaResultados(self):
        """Cria a área que apresenta os resultados dos testes."""

        cartao = ctk.CTkFrame(
            self.areaTestes,
            fg_color=self.corCartao,
            corner_radius=12
        )

        cartao.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=10
        )

        cartao.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            cartao,
            text="Resultados dos testes",
            font=("Arial", 17, "bold"),
            text_color=self.corTexto
        )

        titulo.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 10)
        )

        self.resultadoTestes = ctk.CTkTextbox(
            cartao,
            height=180,
            corner_radius=8,
            fg_color="#171B27",
            text_color=self.corTexto,
            font=("Consolas", 12),
            wrap="word"
        )

        self.resultadoTestes.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 18)
        )

        self.resultadoTestes.insert(
            "1.0",
            "Nenhum teste foi executado ainda.\n\n"
            "Os resultados das operações aparecerão aqui."
        )

    def registrarResultado(self, titulo, resultados):
        """Registra os resultados de uma execução na interface."""

        self.resultadoTestes.delete("1.0", "end")

        textoResultado = f"{titulo}\n"
        textoResultado += "=" * 45 + "\n\n"

        for descricao, aprovado in resultados:
            situacao = "APROVADO" if aprovado else "FALHOU"

            textoResultado += (
                f"[{situacao}] {descricao}\n\n"
            )

        self.resultadoTestes.insert(
            "1.0",
            textoResultado
        )

    def testarIntegridade(self):
        """Testa a integridade de uma mensagem criptografada."""

        senhaDestinatario = self.senhaIntegridade.get()

        if not senhaDestinatario:
            messagebox.showwarning(
                "Senha não informada",
                "Informe a senha da chave privada do destinatário."
            )
            return

        mensagemOriginal = (
            "Esta é uma mensagem utilizada para testar a integridade."
        )

        try:
            dadosCriptografados = criptografarMensagem(
                mensagemOriginal
            )

            mensagemRecuperada = descriptografarMensagem(
                dadosCriptografados,
                senhaDestinatario
            )

            testeOriginal = mensagemRecuperada == mensagemOriginal

            dadosAdulterados = copy.deepcopy(dadosCriptografados)

            mensagemCodificada = base64.b64decode(
                dadosAdulterados["mensagemCriptografada"]
            )

            mensagemAlterada = bytearray(mensagemCodificada)
            mensagemAlterada[0] ^= 1

            dadosAdulterados["mensagemCriptografada"] = (
                base64.b64encode(mensagemAlterada).decode("utf-8")
            )

            adulteracaoDetectada = False

            try:
                descriptografarMensagem(
                    dadosAdulterados,
                    senhaDestinatario
                )

            except Exception:
                adulteracaoDetectada = True

            resultados = [
                (
                    "Mensagem original descriptografada corretamente.",
                    testeOriginal
                ),
                (
                    "Adulteração dos dados criptografados detectada.",
                    adulteracaoDetectada
                )
            ]

            self.registrarResultado(
                "TESTE DE INTEGRIDADE",
                resultados
            )

            if all(aprovado for descricao, aprovado in resultados):
                messagebox.showinfo(
                    "Teste concluído",
                    "Todos os testes de integridade foram aprovados!"
                )
            else:
                messagebox.showwarning(
                    "Resultado do teste",
                    "Um ou mais testes de integridade falharam."
                )

        except Exception as erro:
            messagebox.showerror(
                "Erro no teste de integridade",
                str(erro)
            )

    def testarAssinatura(self):
        """Testa a validação de uma assinatura digital."""

        senhaRemetente = self.senhaAssinatura.get()

        if not senhaRemetente:
            messagebox.showwarning(
                "Senha não informada",
                "Informe a senha da chave privada do remetente."
            )
            return

        mensagemOriginal = (
            "Esta é uma mensagem utilizada para testar a assinatura digital."
        )

        mensagemAdulterada = (
            mensagemOriginal + " Conteúdo alterado."
        )

        try:
            assinaturaBase64 = assinarMensagem(
                mensagemOriginal,
                senhaRemetente
            )

            assinaturaOriginalValida = verificarAssinatura(
                mensagemOriginal,
                assinaturaBase64
            )

            assinaturaAdulteradaInvalida = not verificarAssinatura(
                mensagemAdulterada,
                assinaturaBase64
            )

            resultados = [
                (
                    "Assinatura da mensagem original validada.",
                    assinaturaOriginalValida
                ),
                (
                    "Alteração da mensagem identificada pela assinatura.",
                    assinaturaAdulteradaInvalida
                )
            ]

            self.registrarResultado(
                "TESTE DE ASSINATURA DIGITAL",
                resultados
            )

            if all(aprovado for descricao, aprovado in resultados):
                messagebox.showinfo(
                    "Teste concluído",
                    "Todos os testes de assinatura foram aprovados!"
                )
            else:
                messagebox.showwarning(
                    "Resultado do teste",
                    "Um ou mais testes de assinatura falharam."
                )

        except Exception as erro:
            messagebox.showerror(
                "Erro no teste de assinatura",
                str(erro)
            )