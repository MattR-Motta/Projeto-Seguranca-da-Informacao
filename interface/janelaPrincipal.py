import customtkinter as ctk
from interface.gerenciadorChaves import GerenciadorChaves
from interface.comunicacao import Comunicacao
from interface.testesSeguranca import TestesSeguranca

class JanelaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MensagemSegura")
        self.geometry("1100x700")
        self.minsize(900, 600)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.corFundo = "#10131C"
        self.corMenu = "#171B27"
        self.corCartao = "#1E2433"
        self.corPrimaria = "#5146D8"
        self.corTexto = "#FFFFFF"
        self.corTextoSecundario = "#A7AEC0"

        self.configure(fg_color=self.corFundo)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criarMenuLateral()
        self.criarAreaPrincipal()

        self.mostrarPagina("inicio")

    def criarMenuLateral(self):
        """Cria o menu lateral de navegação."""

        self.menuLateral = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color=self.corMenu
        )

        self.menuLateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.menuLateral.grid_propagate(False)

        self.tituloSistema = ctk.CTkLabel(
            self.menuLateral,
            text="MensagemSegura",
            font=("Arial", 22, "bold"),
            text_color=self.corTexto
        )

        self.tituloSistema.pack(
            padx=20,
            pady=(35, 5)
        )

        self.subtituloSistema = ctk.CTkLabel(
            self.menuLateral,
            text="Sistema de comunicação segura",
            font=("Arial", 11),
            text_color=self.corTextoSecundario
        )

        self.subtituloSistema.pack(
            padx=15,
            pady=(0, 35)
        )

        self.botoesMenu = {}

        opcoesMenu = [
            ("Início", "inicio"),
            ("Comunicação", "comunicacao"),
            ("Gerenciar chaves", "chaves"),
            ("Testes de segurança", "testes")
        ]

        for tituloBotao, pagina in opcoesMenu:
            botao = ctk.CTkButton(
                self.menuLateral,
                text=tituloBotao,
                height=42,
                anchor="w",
                corner_radius=8,
                fg_color="transparent",
                hover_color=self.corCartao,
                text_color=self.corTextoSecundario,
                font=("Arial", 13),
                command=lambda paginaAtual=pagina: self.mostrarPagina(
                    paginaAtual
                )
            )

            botao.pack(
                fill="x",
                padx=15,
                pady=5
            )

            self.botoesMenu[pagina] = botao

        self.rodapeMenu = ctk.CTkLabel(
            self.menuLateral,
            text="MensagemSegura | 2026",
            font=("Arial", 10),
            text_color=self.corTextoSecundario
        )

        self.rodapeMenu.pack(
            side="bottom",
            pady=20
        )

    def criarAreaPrincipal(self):
        """Cria a área onde as páginas serão exibidas."""

        self.areaPrincipal = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.corFundo
        )

        self.areaPrincipal.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=25,
            pady=25
        )

        self.areaPrincipal.grid_columnconfigure(0, weight=1)
        self.areaPrincipal.grid_rowconfigure(0, weight=1)

    def limparAreaPrincipal(self):
        """Remove os elementos da página atualmente exibida."""

        for componente in self.areaPrincipal.winfo_children():
            componente.destroy()

    def atualizarMenu(self, paginaSelecionada):
        """Destaca a opção selecionada no menu."""

        for pagina, botao in self.botoesMenu.items():

            if pagina == paginaSelecionada:
                botao.configure(
                    fg_color=self.corPrimaria,
                    text_color=self.corTexto
                )
            else:
                botao.configure(
                    fg_color="transparent",
                    text_color=self.corTextoSecundario
                )

    def mostrarPagina(self, pagina):
        """Controla a navegação entre as páginas."""

        self.limparAreaPrincipal()
        self.atualizarMenu(pagina)

        if pagina == "inicio":
            self.mostrarInicio()

        elif pagina == "comunicacao":
            self.telaComunicacao = Comunicacao(
                self.areaPrincipal
            )

            self.telaComunicacao.pack(
                fill="both",
                expand=True
            )

        elif pagina == "chaves":
            self.telaGerenciadorChaves = GerenciadorChaves(
                self.areaPrincipal
            )

            self.telaGerenciadorChaves.pack(
                fill="both",
                expand=True
            )

        elif pagina == "testes":
            self.telaTestesSeguranca = TestesSeguranca(
                self.areaPrincipal
            )

            self.telaTestesSeguranca.pack(
                fill="both",
                expand=True
            )

    def mostrarInicio(self):
        """Exibe a página inicial do sistema."""

        titulo = ctk.CTkLabel(
            self.areaPrincipal,
            text="Bem-vindo ao MensagemSegura!",
            font=("Arial", 28, "bold"),
            text_color=self.corTexto
        )

        titulo.pack(
            anchor="w",
            pady=(35, 10)
        )

        descricao = ctk.CTkLabel(
            self.areaPrincipal,
            text=(
                "Uma aplicação para proteger mensagens por meio "
                "de criptografia e assinatura digital."
            ),
            font=("Arial", 14),
            text_color=self.corTextoSecundario,
            wraplength=750,
            justify="left"
        )

        descricao.pack(
            anchor="w",
            pady=(0, 35)
        )

        tituloRecursos = ctk.CTkLabel(
            self.areaPrincipal,
            text="Recursos disponíveis",
            font=("Arial", 19, "bold"),
            text_color=self.corTexto
        )

        tituloRecursos.pack(
            anchor="w",
            pady=(0, 15)
        )

        self.criarCartao(
            "Criptografia híbrida",
            "Proteção das mensagens com AES-256-GCM "
            "e encapsulamento da chave com RSA-OAEP."
        )

        self.criarCartao(
            "Assinatura digital",
            "Verificação de autenticidade utilizando "
            "RSA-PSS e SHA-256."
        )

        self.criarCartao(
            "Integridade",
            "Detecção de alterações nas mensagens "
            "por meio da autenticação AES-GCM."
        )

        aviso = ctk.CTkLabel(
            self.areaPrincipal,
            text=(
                "Selecione uma opção no menu lateral para "
                "acessar as funcionalidades do sistema."
            ),
            font=("Arial", 12),
            text_color=self.corTextoSecundario
        )

        aviso.pack(
            anchor="w",
            pady=(30, 0)
        )

    def criarCartao(self, tituloCartao, descricaoCartao):
        """Cria um cartão informativo na página inicial."""

        cartao = ctk.CTkFrame(
            self.areaPrincipal,
            fg_color=self.corCartao,
            corner_radius=12
        )

        cartao.pack(
            fill="x",
            pady=7
        )

        titulo = ctk.CTkLabel(
            cartao,
            text=tituloCartao,
            font=("Arial", 16, "bold"),
            text_color=self.corTexto
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        descricao = ctk.CTkLabel(
            cartao,
            text=descricaoCartao,
            font=("Arial", 12),
            text_color=self.corTextoSecundario,
            wraplength=700,
            justify="left"
        )

        descricao.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

    def mostrarPaginaEmConstrucao(self, tituloPagina, descricaoPagina):
        """Exibe uma mensagem temporária para páginas não integradas."""

        titulo = ctk.CTkLabel(
            self.areaPrincipal,
            text=tituloPagina,
            font=("Arial", 26, "bold"),
            text_color=self.corTexto
        )

        titulo.pack(
            anchor="w",
            pady=(35, 10)
        )

        descricao = ctk.CTkLabel(
            self.areaPrincipal,
            text=descricaoPagina,
            font=("Arial", 14),
            text_color=self.corTextoSecundario
        )

        descricao.pack(
            anchor="w",
            pady=(0, 20)
        )

        aviso = ctk.CTkLabel(
            self.areaPrincipal,
            text="Esta funcionalidade será integrada nas próximas etapas.",
            font=("Arial", 12),
            text_color=self.corTextoSecundario
        )

        aviso.pack(
            anchor="w",
            pady=10
        )