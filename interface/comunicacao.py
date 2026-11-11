import json
import customtkinter as ctk
from tkinter import messagebox

from seguranca.criptografia import criptografarMensagem
from seguranca.descriptografia import descriptografarMensagem
from seguranca.assinatura import assinarMensagem, verificarAssinatura


class Comunicacao(ctk.CTkFrame):
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

        self.criarInterface()

    def criarInterface(self):
        """Monta as áreas de envio e recebimento de mensagens."""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        titulo = ctk.CTkLabel(
            self,
            text="Comunicação segura",
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
            text="Criptografe, assine, receba e verifique mensagens.",
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

        self.abas = ctk.CTkTabview(
            self,
            fg_color=self.corCartao,
            segmented_button_selected_color=self.corPrimaria,
            segmented_button_selected_hover_color="#4035B5"
        )

        self.abas.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(5, 20)
        )

        self.abaEnvio = self.abas.add("Enviar mensagem")
        self.abaRecebimento = self.abas.add("Receber mensagem")

        self.criarAbaEnvio()
        self.criarAbaRecebimento()

    def criarAbaEnvio(self):
        """Cria a área de escrita, assinatura e criptografia."""

        self.abaEnvio.grid_columnconfigure(0, weight=1)
        self.abaEnvio.grid_rowconfigure(0, weight=1)

        self.conteudoEnvio = ctk.CTkScrollableFrame(
            self.abaEnvio,
            fg_color="transparent"
        )

        self.conteudoEnvio.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.conteudoEnvio.grid_columnconfigure(0, weight=1)

        tituloMensagem = ctk.CTkLabel(
            self.conteudoEnvio,
            text="Mensagem original",
            font=("Arial", 15, "bold"),
            text_color=self.corTexto
        )

        tituloMensagem.grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 8)
        )

        self.campoMensagem = ctk.CTkTextbox(
            self.conteudoEnvio,
            height=130,
            corner_radius=8,
            fg_color="#171B27",
            text_color=self.corTexto,
            font=("Arial", 13)
        )

        self.campoMensagem.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=5
        )

        tituloSenha = ctk.CTkLabel(
            self.conteudoEnvio,
            text="Senha da chave privada do remetente",
            font=("Arial", 13),
            text_color=self.corTexto
        )

        tituloSenha.grid(
            row=2,
            column=0,
            sticky="w",
            padx=10,
            pady=(15, 5)
        )

        self.senhaRemetente = ctk.CTkEntry(
            self.conteudoEnvio,
            placeholder_text="Digite a senha da chave de assinatura",
            show="*",
            height=40,
            width=400
        )

        self.senhaRemetente.grid(
            row=3,
            column=0,
            sticky="w",
            padx=10,
            pady=5
        )

        botaoEnviar = ctk.CTkButton(
            self.conteudoEnvio,
            text="Criptografar e assinar mensagem",
            height=42,
            fg_color=self.corPrimaria,
            hover_color="#4035B5",
            command=self.criptografarEAssinar
        )

        botaoEnviar.grid(
            row=4,
            column=0,
            sticky="w",
            padx=10,
            pady=15
        )

        tituloResultado = ctk.CTkLabel(
            self.conteudoEnvio,
            text="Dados para compartilhamento",
            font=("Arial", 15, "bold"),
            text_color=self.corTexto
        )

        tituloResultado.grid(
            row=5,
            column=0,
            sticky="w",
            padx=10,
            pady=(5, 8)
        )

        self.resultadoEnvio = ctk.CTkTextbox(
            self.conteudoEnvio,
            height=160,
            corner_radius=8,
            fg_color="#171B27",
            text_color=self.corTexto,
            font=("Consolas", 11),
            wrap="word"
        )

        self.resultadoEnvio.grid(
            row=6,
            column=0,
            sticky="ew",
            padx=10,
            pady=5
        )

        botaoCopiar = ctk.CTkButton(
            self.conteudoEnvio,
            text="Copiar dados",
            height=36,
            fg_color="#343B50",
            hover_color="#424B65",
            command=self.copiarDados
        )

        botaoCopiar.grid(
            row=7,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 15)
        )

    def criarAbaRecebimento(self):
        """Cria a área de recebimento e verificação."""

        self.abaRecebimento.grid_columnconfigure(0, weight=1)
        self.abaRecebimento.grid_rowconfigure(0, weight=1)

        self.conteudoRecebimento = ctk.CTkScrollableFrame(
            self.abaRecebimento,
            fg_color="transparent"
        )

        self.conteudoRecebimento.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.conteudoRecebimento.grid_columnconfigure(0, weight=1)

        tituloDados = ctk.CTkLabel(
            self.conteudoRecebimento,
            text="Dados recebidos",
            font=("Arial", 15, "bold"),
            text_color=self.corTexto
        )

        tituloDados.grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 8)
        )

        self.campoDadosRecebidos = ctk.CTkTextbox(
            self.conteudoRecebimento,
            height=180,
            corner_radius=8,
            fg_color="#171B27",
            text_color=self.corTexto,
            font=("Consolas", 11),
            wrap="word"
        )

        self.campoDadosRecebidos.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=5
        )

        tituloSenha = ctk.CTkLabel(
            self.conteudoRecebimento,
            text="Senha da chave privada do destinatário",
            font=("Arial", 13),
            text_color=self.corTexto
        )

        tituloSenha.grid(
            row=2,
            column=0,
            sticky="w",
            padx=10,
            pady=(15, 5)
        )

        self.senhaDestinatario = ctk.CTkEntry(
            self.conteudoRecebimento,
            placeholder_text="Digite a senha da chave de descriptografia",
            show="*",
            height=40,
            width=400
        )

        self.senhaDestinatario.grid(
            row=3,
            column=0,
            sticky="w",
            padx=10,
            pady=5
        )

        botaoReceber = ctk.CTkButton(
            self.conteudoRecebimento,
            text="Descriptografar e verificar assinatura",
            height=42,
            fg_color=self.corPrimaria,
            hover_color="#4035B5",
            command=self.descriptografarEVerificar
        )

        botaoReceber.grid(
            row=4,
            column=0,
            sticky="w",
            padx=10,
            pady=15
        )

        tituloResultado = ctk.CTkLabel(
            self.conteudoRecebimento,
            text="Resultado da operação",
            font=("Arial", 15, "bold"),
            text_color=self.corTexto
        )

        tituloResultado.grid(
            row=5,
            column=0,
            sticky="w",
            padx=10,
            pady=(5, 8)
        )

        self.resultadoRecebimento = ctk.CTkTextbox(
            self.conteudoRecebimento,
            height=150,
            corner_radius=8,
            fg_color="#171B27",
            text_color=self.corTexto,
            font=("Arial", 12),
            wrap="word"
        )

        self.resultadoRecebimento.grid(
            row=6,
            column=0,
            sticky="ew",
            padx=10,
            pady=(5, 15)
        )

    def criptografarEAssinar(self):
        """Criptografa e assina a mensagem antes do envio."""

        mensagemOriginal = self.campoMensagem.get(
            "1.0",
            "end"
        ).strip()

        senhaRemetente = self.senhaRemetente.get()

        if not mensagemOriginal:
            messagebox.showwarning(
                "Mensagem vazia",
                "Digite uma mensagem antes de continuar."
            )
            return

        if not senhaRemetente:
            messagebox.showwarning(
                "Senha não informada",
                "Informe a senha da chave privada do remetente."
            )
            return

        try:
            dadosCriptografados = criptografarMensagem(
                mensagemOriginal
            )

            assinaturaBase64 = assinarMensagem(
                mensagemOriginal,
                senhaRemetente
            )

            pacoteMensagem = {
                "versao": "1.0",
                "dadosCriptografados": dadosCriptografados,
                "assinatura": assinaturaBase64
            }

            resultadoJson = json.dumps(
                pacoteMensagem,
                ensure_ascii=False,
                indent=4
            )

            self.resultadoEnvio.delete("1.0", "end")
            self.resultadoEnvio.insert("1.0", resultadoJson)

            messagebox.showinfo(
                "Mensagem protegida",
                "A mensagem foi criptografada e assinada com sucesso!"
            )

        except (ValueError, FileNotFoundError, OSError) as erro:
            messagebox.showerror(
                "Erro ao proteger mensagem",
                str(erro)
            )

    def copiarDados(self):
        """Copia o pacote JSON para a área de transferência."""

        dados = self.resultadoEnvio.get(
            "1.0",
            "end"
        ).strip()

        if not dados:
            messagebox.showwarning(
                "Nenhum dado",
                "Não existem dados para copiar."
            )
            return

        self.clipboard_clear()
        self.clipboard_append(dados)
        self.update()

        messagebox.showinfo(
            "Dados copiados",
            "Os dados protegidos foram copiados."
        )

    def descriptografarEVerificar(self):
        """Descriptografa a mensagem e verifica sua assinatura."""

        dadosTexto = self.campoDadosRecebidos.get(
            "1.0",
            "end"
        ).strip()

        senhaDestinatario = self.senhaDestinatario.get()

        if not dadosTexto:
            messagebox.showwarning(
                "Dados não informados",
                "Insira os dados recebidos para continuar."
            )
            return

        if not senhaDestinatario:
            messagebox.showwarning(
                "Senha não informada",
                "Informe a senha da chave privada do destinatário."
            )
            return

        try:
            pacoteMensagem = json.loads(dadosTexto)

            if not isinstance(pacoteMensagem, dict):
                raise ValueError(
                    "O pacote recebido possui formato inválido."
                )

            if pacoteMensagem.get("versao") != "1.0":
                raise ValueError(
                    "Versão do pacote não reconhecida."
                )

            dadosCriptografados = pacoteMensagem.get(
                "dadosCriptografados"
            )

            assinaturaBase64 = pacoteMensagem.get("assinatura")

            if not isinstance(dadosCriptografados, dict):
                raise ValueError(
                    "Os dados criptografados estão ausentes."
                )

            if not isinstance(assinaturaBase64, str):
                raise ValueError(
                    "A assinatura digital está ausente."
                )

            mensagemOriginal = descriptografarMensagem(
                dadosCriptografados,
                senhaDestinatario
            )

            assinaturaValida = verificarAssinatura(
                mensagemOriginal,
                assinaturaBase64
            )

            self.resultadoRecebimento.delete("1.0", "end")

            self.resultadoRecebimento.insert(
                "1.0",
                "MENSAGEM DESCRIPTOGRAFADA COM SUCESSO!\n\n"
                f"Mensagem original:\n{mensagemOriginal}\n\n"
            )

            if assinaturaValida:
                self.resultadoRecebimento.insert(
                    "end",
                    "ASSINATURA DIGITAL: VÁLIDA\n"
                    "A assinatura corresponde à mensagem e à chave pública utilizada."
                )

                messagebox.showinfo(
                    "Mensagem verificada",
                    "A mensagem foi recuperada e a assinatura é válida."
                )

            else:
                self.resultadoRecebimento.insert(
                    "end",
                    "ASSINATURA DIGITAL: INVÁLIDA\n"
                    "Não foi possível validar a assinatura do remetente."
                )

                messagebox.showwarning(
                    "Assinatura inválida",
                    "A mensagem foi descriptografada, mas sua assinatura não é válida."
                )

        except json.JSONDecodeError:
            messagebox.showerror(
                "Formato inválido",
                "Os dados recebidos não formam um JSON válido."
            )

        except (ValueError, FileNotFoundError, OSError) as erro:
            self.resultadoRecebimento.delete("1.0", "end")

            self.resultadoRecebimento.insert(
                "1.0",
                f"Falha na operação:\n{erro}"
            )

            messagebox.showerror(
                "Erro ao receber mensagem",
                str(erro)
            )