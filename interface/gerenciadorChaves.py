from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
from seguranca.gerarChaves import gerarParChaves
from seguranca.assinatura import gerarParChavesAssinatura

class GerenciadorChaves(ctk.CTkFrame):
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

        self.pastaChaves = (
            Path(__file__).resolve().parent.parent
            / "dados"
            / "chaves"
        )

        self.senhaChave = None

        self.criarInterface()
        self.atualizarStatusChaves()

    def criarInterface(self):
        """Monta os componentes da tela de gerenciamento."""

        self.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            self,
            text="Gerenciamento de chaves",
            font=("Arial", 26, "bold"),
            text_color=self.corTexto
        )

        titulo.grid(
            row=0,
            column=0,
            sticky="w",
            padx=30,
            pady=(30, 8)
        )

        descricao = ctk.CTkLabel(
            self,
            text=(
                "Gerencie os pares de chaves utilizados para "
                "proteger e autenticar as mensagens."
            ),
            font=("Arial", 13),
            text_color=self.corTextoSecundario
        )

        descricao.grid(
            row=1,
            column=0,
            sticky="w",
            padx=30,
            pady=(0, 25)
        )

        # Área de geração das chaves
        cartaoGeracao = ctk.CTkFrame(
            self,
            fg_color=self.corCartao,
            corner_radius=12
        )

        cartaoGeracao.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=30,
            pady=10
        )

        cartaoGeracao.grid_columnconfigure(0, weight=1)

        tituloGeracao = ctk.CTkLabel(
            cartaoGeracao,
            text="Gerar pares de chaves",
            font=("Arial", 18, "bold"),
            text_color=self.corTexto
        )

        tituloGeracao.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 8)
        )

        descricaoGeracao = ctk.CTkLabel(
            cartaoGeracao,
            text=(
                "Informe uma senha para proteger as chaves privadas. "
                "Utilize pelo menos 8 caracteres."
            ),
            font=("Arial", 12),
            text_color=self.corTextoSecundario,
            wraplength=650,
            justify="left"
        )

        descricaoGeracao.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 15)
        )

        self.campoSenha = ctk.CTkEntry(
            cartaoGeracao,
            placeholder_text="Digite uma senha",
            show="*",
            height=42,
            width=350
        )

        self.campoSenha.grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=5
        )

        self.campoConfirmacao = ctk.CTkEntry(
            cartaoGeracao,
            placeholder_text="Confirme a senha",
            show="*",
            height=42,
            width=350
        )

        self.campoConfirmacao.grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=5
        )

        self.botaoDestinatario = ctk.CTkButton(
            cartaoGeracao,
            text="Gerar chaves do destinatário",
            height=42,
            fg_color=self.corPrimaria,
            hover_color="#4035B5",
            command=self.gerarChavesDestinatario
        )

        self.botaoDestinatario.grid(
            row=4,
            column=0,
            sticky="w",
            padx=20,
            pady=(15, 8)
        )

        self.botaoRemetente = ctk.CTkButton(
            cartaoGeracao,
            text="Gerar chaves do remetente",
            height=42,
            fg_color=self.corPrimaria,
            hover_color="#4035B5",
            command=self.gerarChavesRemetente
        )

        self.botaoRemetente.grid(
            row=5,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 20)
        )

        # Área de consulta dos pares existentes
        cartaoStatus = ctk.CTkFrame(
            self,
            fg_color=self.corCartao,
            corner_radius=12
        )

        cartaoStatus.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=30,
            pady=10
        )

        cartaoStatus.grid_columnconfigure(0, weight=1)

        tituloStatus = ctk.CTkLabel(
            cartaoStatus,
            text="Status dos pares de chaves",
            font=("Arial", 18, "bold"),
            text_color=self.corTexto
        )

        tituloStatus.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 15)
        )

        self.statusDestinatario = ctk.CTkLabel(
            cartaoStatus,
            text="Chaves do destinatário: verificando...",
            font=("Arial", 13),
            text_color=self.corTextoSecundario
        )

        self.statusDestinatario.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=8
        )

        self.statusRemetente = ctk.CTkLabel(
            cartaoStatus,
            text="Chaves do remetente: verificando...",
            font=("Arial", 13),
            text_color=self.corTextoSecundario
        )

        self.statusRemetente.grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=8
        )

        botaoAtualizar = ctk.CTkButton(
            cartaoStatus,
            text="Atualizar status",
            height=36,
            fg_color="#343B50",
            hover_color="#424B65",
            command=self.atualizarStatusChaves
        )

        botaoAtualizar.grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=(15, 20)
        )

        # Orientação sobre segurança
        aviso = ctk.CTkLabel(
            self,
            text=(
                "Importante: nunca compartilhe suas chaves privadas. "
                "Compartilhe somente as chaves públicas quando necessário."
            ),
            font=("Arial", 12),
            text_color="#E5B85C",
            wraplength=700,
            justify="left"
        )

        aviso.grid(
            row=4,
            column=0,
            sticky="w",
            padx=30,
            pady=15
        )

    def obterSenha(self):
        """Valida e retorna a senha informada pelo usuário."""

        senhaChave = self.campoSenha.get()
        confirmacaoSenha = self.campoConfirmacao.get()

        if len(senhaChave) < 8:
            messagebox.showwarning(
                "Senha inválida",
                "A senha deve possuir pelo menos 8 caracteres."
            )
            return None

        if senhaChave != confirmacaoSenha:
            messagebox.showwarning(
                "Senhas diferentes",
                "A confirmação da senha não corresponde à senha informada."
            )
            return None

        return senhaChave

    def gerarChavesDestinatario(self):
        """Gera o par RSA utilizado na criptografia."""

        senhaChave = self.obterSenha()

        if senhaChave is None:
            return

        try:
            gerarParChaves(senhaChave)

            messagebox.showinfo(
                "Sucesso",
                "Par de chaves do destinatário gerado com sucesso!"
            )

            self.campoSenha.delete(0, "end")
            self.campoConfirmacao.delete(0, "end")

            self.atualizarStatusChaves()

        except FileExistsError as erro:
            messagebox.showwarning(
                "Chaves existentes",
                str(erro)
            )

        except (ValueError, OSError) as erro:
            messagebox.showerror(
                "Erro ao gerar chaves",
                str(erro)
            )

    def gerarChavesRemetente(self):
        """Gera o par RSA utilizado na assinatura digital."""

        senhaChave = self.obterSenha()

        if senhaChave is None:
            return

        try:
            gerarParChavesAssinatura(senhaChave)

            messagebox.showinfo(
                "Sucesso",
                "Par de chaves do remetente gerado com sucesso!"
            )

            self.campoSenha.delete(0, "end")
            self.campoConfirmacao.delete(0, "end")

            self.atualizarStatusChaves()

        except FileExistsError as erro:
            messagebox.showwarning(
                "Chaves existentes",
                str(erro)
            )

        except (ValueError, OSError) as erro:
            messagebox.showerror(
                "Erro ao gerar chaves",
                str(erro)
            )

    def atualizarStatusChaves(self):
        """Verifica a existência dos arquivos de chaves."""

        chavePrivadaDestinatario = (
            self.pastaChaves / "destinatario_private.pem"
        )

        chavePublicaDestinatario = (
            self.pastaChaves / "destinatario_public.pem"
        )

        chavePrivadaRemetente = (
            self.pastaChaves / "remetente_private.pem"
        )

        chavePublicaRemetente = (
            self.pastaChaves / "remetente_public.pem"
        )

        destinatarioCompleto = (
            chavePrivadaDestinatario.is_file()
            and chavePublicaDestinatario.is_file()
        )

        remetenteCompleto = (
            chavePrivadaRemetente.is_file()
            and chavePublicaRemetente.is_file()
        )

        if destinatarioCompleto:
            textoDestinatario = "Chaves do destinatário: disponíveis"
            corDestinatario = "#55D68B"
        else:
            textoDestinatario = "Chaves do destinatário: não geradas ou incompletas"
            corDestinatario = "#E5B85C"

        if remetenteCompleto:
            textoRemetente = "Chaves do remetente: disponíveis"
            corRemetente = "#55D68B"
        else:
            textoRemetente = "Chaves do remetente: não geradas ou incompletas"
            corRemetente = "#E5B85C"

        self.statusDestinatario.configure(
            text=textoDestinatario,
            text_color=corDestinatario
        )

        self.statusRemetente.configure(
            text=textoRemetente,
            text_color=corRemetente
        )
