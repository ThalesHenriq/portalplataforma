import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Optional, List
import time

# Configuração da página
st.set_page_config(
    page_title="Portal de Plataformas",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== CLASSES DE USUÁRIO E AUTENTICAÇÃO ==========

@dataclass
class Usuario:
    id: str
    nome: str
    email: str
    senha_hash: str
    tipo: str  # "admin" ou "usuario"
    plataformas_autorizadas: List[str]
    data_criacao: str
    ultimo_acesso: Optional[str] = None

class GerenciadorUsuarios:
    def __init__(self, arquivo_usuarios="usuarios.json"):
        self.arquivo_usuarios = arquivo_usuarios
        self.carregar_usuarios()
        
        # Criar admin padrão se não existir
        if not self.usuarios:
            self.criar_usuario_padrao()
    
    def carregar_usuarios(self):
        """Carrega usuários do arquivo JSON"""
        if os.path.exists(self.arquivo_usuarios):
            with open(self.arquivo_usuarios, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.usuarios = [Usuario(**u) for u in dados]
        else:
            self.usuarios = []
    
    def salvar_usuarios(self):
        """Salva usuários no arquivo JSON"""
        with open(self.arquivo_usuarios, 'w', encoding='utf-8') as f:
            dados = [u.__dict__ for u in self.usuarios]
            json.dump(dados, f, indent=4, ensure_ascii=False)
    
    def criar_usuario_padrao(self):
        """Cria um usuário administrador padrão"""
        senha_hash = hashlib.sha256("admin123".encode()).hexdigest()
        admin = Usuario(
            id=f"USR{datetime.now().strftime('%Y%m%d%H%M%S')}",
            nome="Administrador",
            email="admin@sistema.com",
            senha_hash=senha_hash,
            tipo="admin",
            plataformas_autorizadas=["todas"],
            data_criacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.usuarios.append(admin)
        self.salvar_usuarios()
    
    def autenticar(self, email: str, senha: str) -> Optional[Usuario]:
        """Autentica um usuário"""
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha_hash == senha_hash:
                usuario.ultimo_acesso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.salvar_usuarios()
                return usuario
        return None
    
    def criar_usuario(self, nome: str, email: str, senha: str, tipo: str, plataformas: List[str]):
        """Cria um novo usuário"""
        # Verificar se email já existe
        if any(u.email == email for u in self.usuarios):
            return False, "Email já cadastrado"
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        novo_usuario = Usuario(
            id=f"USR{datetime.now().strftime('%Y%m%d%H%M%S')}",
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            tipo=tipo,
            plataformas_autorizadas=plataformas,
            data_criacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.usuarios.append(novo_usuario)
        self.salvar_usuarios()
        return True, "Usuário criado com sucesso"

# ========== DEFINIÇÃO DAS PLATAFORMAS ==========

class Plataforma:
    def __init__(self, id, nome, icone, cor, descricao, modulo, link_externo=None):
        self.id = id
        self.nome = nome
        self.icone = icone
        self.cor = cor
        self.descricao = descricao
        self.modulo = modulo
        self.link_externo = link_externo

# Lista de plataformas disponíveis
PLATAFORMAS = [
    Plataforma(
        id="agendamento",
        nome="Sistema de Agendamento",
        icone="📅",
        cor="#FF4B4B",
        descricao="Gerencie agendamentos, horários e serviços",
        modulo="agendamento"
    ),
    Plataforma(
        id="vendas",
        nome="Sistema de Vendas",
        icone="💰",
        cor="#00CC96",
        descricao="Controle de vendas, estoque e clientes",
        modulo="vendas"
    ),
    Plataforma(
        id="financeiro",
        nome="Sistema Financeiro",
        icone="📊",
        cor="#FFA500",
        descricao="Fluxo de caixa, contas a pagar/receber",
        modulo="financeiro"
    ),
    Plataforma(
        id="rh",
        nome="Sistema de RH",
        icone="👥",
        cor="#6C3483",
        descricao="Gestão de funcionários e folha de pagamento",
        modulo="rh"
    ),
    Plataforma(
        id="estoque",
        nome="Sistema de Estoque",
        icone="📦",
        cor="#3498DB",
        descricao="Controle de estoque e fornecedores",
        modulo="estoque"
    ),
    Plataforma(
        id="holerite",
        nome="Sistema de Holerite",
        icone="📄",
        cor="#27AE60",
        descricao="Os cálculos usam regras aproximadas de 2026 (INSS e IRRF). Para uso profissional, valide com contador",
        modulo="holerite_externo",  # Nome diferente para não conflitar
        link_externo="https://holeriteon-dlxxg3jqgtz25q9tf4wn7z.streamlit.app/"
    ),
    Plataforma(
        id="relatorios",
        nome="Sistema de Relatórios",
        icone="📈",
        cor="#E74C3C",
        descricao="Relatórios gerenciais e indicadores",
        modulo="relatorios"
    )
]

# ========== MÓDULOS DAS PLATAFORMAS ==========

def modulo_agendamento():
    """Módulo do Sistema de Agendamento"""
    st.header("📅 Sistema de Agendamento")
    
    # Simulação de dados
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Agendamentos Hoje", "12", "+2")
    with col2:
        st.metric("Agendamentos Semana", "45", "+5")
    with col3:
        st.metric("Taxa de Ocupação", "78%", "-3%")
    with col4:
        st.metric("Cancelamentos", "3", "-1")
    
    # Tabela de agendamentos
    st.subheader("Próximos Agendamentos")
    dados_agendamentos = pd.DataFrame({
        "Cliente": ["João Silva", "Maria Santos", "Carlos Oliveira", "Ana Souza"],
        "Serviço": ["Corte", "Manicure", "Barba", "Coloração"],
        "Profissional": ["Carlos", "Ana", "João", "Maria"],
        "Data/Hora": ["14:30", "15:00", "15:30", "16:00"],
        "Status": ["Confirmado", "Confirmado", "Em espera", "Confirmado"]
    })
    st.dataframe(dados_agendamentos, use_container_width=True, hide_index=True)

def modulo_vendas():
    """Módulo do Sistema de Vendas"""
    st.header("💰 Sistema de Vendas")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Vendas Hoje", "R$ 2.450", "+12%")
    with col2:
        st.metric("Vendas Mês", "R$ 45.890", "+8%")
    with col3:
        st.metric("Ticket Médio", "R$ 89,50", "+R$ 5,20")
    
    st.subheader("Últimas Vendas")
    dados_vendas = pd.DataFrame({
        "Cliente": ["Empresa A", "Empresa B", "Cliente C", "Cliente D"],
        "Produto": ["Produto X", "Serviço Y", "Produto Z", "Serviço W"],
        "Valor": ["R$ 1.200", "R$ 850", "R$ 320", "R$ 1.500"],
        "Data": ["10:30", "11:45", "14:20", "15:10"],
        "Status": ["Pago", "Pago", "Pendente", "Pago"]
    })
    st.dataframe(dados_vendas, use_container_width=True, hide_index=True)

def modulo_financeiro():
    """Módulo do Sistema Financeiro"""
    st.header("📊 Sistema Financeiro")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Saldo Atual", "R$ 15.230", "+R$ 2.100")
    with col2:
        st.metric("Contas a Receber", "R$ 8.450", "+3")
    with col3:
        st.metric("Contas a Pagar", "R$ 4.320", "-2")
    with col4:
        st.metric("Fluxo Projetado", "R$ 19.360", "+12%")
    
    # Gráfico simples
    st.subheader("Fluxo de Caixa - Últimos 30 dias")
    dados_fluxo = pd.DataFrame({
        "Dia": list(range(1, 11)),
        "Entradas": [1200, 1350, 1100, 1400, 1550, 1300, 1250, 1400, 1500, 1450],
        "Saídas": [800, 950, 700, 1100, 1050, 900, 850, 950, 1000, 1100]
    })
    st.line_chart(dados_fluxo.set_index("Dia"))

def modulo_rh():
    """Módulo do Sistema de RH"""
    st.header("👥 Sistema de RH")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Funcionários Ativos", "25", "+2")
    with col2:
        st.metric("Horas Trabalhadas", "3.450", "+120")
    with col3:
        st.metric("Afastamentos", "2", "-1")
    with col4:
        st.metric("Treinamentos", "3", "+1")
    
    st.subheader("Próximos Aniversários")
    dados_aniversarios = pd.DataFrame({
        "Funcionário": ["Ana Lima", "Carlos Sousa", "Mariana Silva"],
        "Cargo": ["Analista", "Coordenador", "Assistente"],
        "Data": ["15/05", "18/05", "22/05"],
        "Departamento": ["RH", "Vendas", "Financeiro"]
    })
    st.dataframe(dados_aniversarios, use_container_width=True, hide_index=True)

def modulo_estoque():
    """Módulo do Sistema de Estoque"""
    st.header("📦 Sistema de Estoque")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Itens", "1.234", "+45")
    with col2:
        st.metric("Valor em Estoque", "R$ 45.670", "+R$ 3.200")
    with col3:
        st.metric("Itens em Falta", "8", "-3")
    with col4:
        st.metric("Pedidos Pendentes", "5", "+1")
    
    st.subheader("Produtos com Estoque Baixo")
    dados_estoque = pd.DataFrame({
        "Produto": ["Item A", "Item B", "Item C", "Item D"],
        "Quantidade": [5, 3, 2, 8],
        "Mínimo": [10, 10, 5, 15],
        "Fornecedor": ["Fornecedor X", "Fornecedor Y", "Fornecedor Z", "Fornecedor X"]
    })
    st.dataframe(dados_estoque, use_container_width=True, hide_index=True)

def modulo_holerite_externo():
    """Módulo do Sistema de Holerite - Redireciona para link externo"""
    st.header("📄 Sistema de Holerite")
    
    # Obter o link da plataforma
    plataforma = next(p for p in PLATAFORMAS if p.id == "holerite")
    
    st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #27AE60 0%, #219653 100%);
            padding: 50px;
            border-radius: 20px;
            text-align: center;
            color: white;
            margin: 30px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        '>
            <div style='font-size: 5em; margin-bottom: 20px;'>📄</div>
            <h2 style='color: white; font-size: 2.5em; margin-bottom: 20px;'>Sistema de Holerite</h2>
            <p style='font-size: 1.2em; margin-bottom: 30px; max-width: 600px; margin-left: auto; margin-right: auto;'>
                Este é um sistema externo especializado em cálculos de holerite.
            </p>
            <div style='
                background-color: rgba(255,255,255,0.2);
                padding: 15px;
                border-radius: 10px;
                margin: 20px auto;
                max-width: 500px;
                font-size: 0.95em;
            '>
                ⚠️ <strong>Aviso importante:</strong><br>
                Os cálculos usam regras aproximadas de 2026 (INSS e IRRF).<br>
                Para uso profissional, valide com um contador.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Botões para acesso
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Link button do Streamlit (abre na mesma aba)
        st.link_button(
            "🌐 Abrir Sistema de Holerite (mesma aba)",
            plataforma.link_externo,
            use_container_width=True,
            type="primary"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Link button com target _blank usando HTML (abre em nova aba)
        st.markdown(f"""
            <a href="{plataforma.link_externo}" target="_blank" style="text-decoration: none;">
                <div style='
                    background-color: white;
                    color: #27AE60;
                    padding: 12px 20px;
                    border-radius: 10px;
                    text-align: center;
                    font-weight: bold;
                    border: 2px solid #27AE60;
                    cursor: pointer;
                    transition: all 0.3s;
                '>
                    🔗 Abrir em Nova Aba
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botão para voltar
        if st.button("← Voltar para o Dashboard", use_container_width=True):
            st.session_state.pagina = "dashboard"
            st.rerun()

def modulo_relatorios():
    """Módulo do Sistema de Relatórios"""
    st.header("📈 Sistema de Relatórios")
    
    st.subheader("Relatórios Disponíveis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Relatório de Vendas", use_container_width=True):
            st.info("Gerando relatório de vendas...")
            time.sleep(2)
            st.success("Relatório gerado com sucesso!")
        
        if st.button("👥 Relatório de RH", use_container_width=True):
            st.info("Gerando relatório de RH...")
            time.sleep(2)
            st.success("Relatório gerado com sucesso!")
        
        if st.button("📦 Relatório de Estoque", use_container_width=True):
            st.info("Gerando relatório de estoque...")
            time.sleep(2)
            st.success("Relatório gerado com sucesso!")
    
    with col2:
        if st.button("💰 Relatório Financeiro", use_container_width=True):
            st.info("Gerando relatório financeiro...")
            time.sleep(2)
            st.success("Relatório gerado com sucesso!")
        
        if st.button("📅 Relatório de Agendamentos", use_container_width=True):
            st.info("Gerando relatório de agendamentos...")
            time.sleep(2)
            st.success("Relatório gerado com sucesso!")
        
        if st.button("📈 Relatório de Indicadores", use_container_width=True):
            st.info("Gerando relatório de indicadores...")
            time.sleep(2)
            st.success("Relatório gerado com sucesso!")

# Mapeamento de módulos
MODULOS = {
    "agendamento": modulo_agendamento,
    "vendas": modulo_vendas,
    "financeiro": modulo_financeiro,
    "rh": modulo_rh,
    "estoque": modulo_estoque,
    "holerite_externo": modulo_holerite_externo,  # Nome atualizado
    "relatorios": modulo_relatorios
}

# ========== INTERFACE DE LOGIN ==========

def tela_login():
    """Tela de login do sistema"""
    
    # CSS personalizado
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 40px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .login-title {
            text-align: center;
            color: #333;
            font-size: 2em;
            margin-bottom: 30px;
        }
        .login-subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        /* Garantir que links externos funcionem */
        .stLinkButton {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="login-container">
                <h1 class="login-title">🚀 Portal de Plataformas</h1>
                <p class="login-subtitle">Faça login para acessar todas as plataformas</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("📧 E-mail", placeholder="seu@email.com")
            senha = st.text_input("🔒 Senha", type="password", placeholder="••••••••")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Entrar", type="primary", use_container_width=True)
            with col2:
                if st.form_submit_button("Cadastrar", use_container_width=True):
                    st.session_state.pagina = "cadastro"
                    st.rerun()
            
            if submit:
                if email and senha:
                    usuario = st.session_state.gerenciador_usuarios.autenticar(email, senha)
                    if usuario:
                        st.session_state.usuario_logado = usuario
                        st.session_state.autenticado = True
                        st.success("Login realizado com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("E-mail ou senha inválidos!")
                else:
                    st.warning("Preencha todos os campos!")

def tela_cadastro():
    """Tela de cadastro de usuário"""
    
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("📝 Cadastro de Usuário")
        
        with st.form("cadastro_form"):
            nome = st.text_input("👤 Nome completo")
            email = st.text_input("📧 E-mail")
            senha = st.text_input("🔒 Senha", type="password")
            confirmar_senha = st.text_input("🔒 Confirmar senha", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Cadastrar", type="primary", use_container_width=True):
                    if senha != confirmar_senha:
                        st.error("As senhas não conferem!")
                    elif nome and email and senha:
                        # Por padrão, novos usuários têm acesso a todas as plataformas
                        sucesso, mensagem = st.session_state.gerenciador_usuarios.criar_usuario(
                            nome=nome,
                            email=email,
                            senha=senha,
                            tipo="usuario",
                            plataformas=["todas"]
                        )
                        if sucesso:
                            st.success(mensagem)
                            time.sleep(2)
                            st.session_state.pagina = "login"
                            st.rerun()
                        else:
                            st.error(mensagem)
                    else:
                        st.warning("Preencha todos os campos!")
            
            with col2:
                if st.form_submit_button("Voltar ao Login", use_container_width=True):
                    st.session_state.pagina = "login"
                    st.rerun()

# ========== DASHBOARD PRINCIPAL COM CARDS ==========

def dashboard_principal():
    """Dashboard principal com cards das plataformas"""
    
    # Header com informações do usuário
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.title(f"🚀 Bem-vindo, {st.session_state.usuario_logado.nome}!")
    
    with col2:
        st.write(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    
    with col3:
        if st.button("🚪 Sair", type="secondary"):
            st.session_state.autenticado = False
            st.session_state.usuario_logado = None
            st.session_state.pagina = "login"
            st.rerun()
    
    st.markdown("---")
    
    # Mensagem de boas-vindas
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h2>Selecione uma plataforma para acessar</h2>
            <p style='color: #666;'>Você tem acesso a todas as 7 plataformas do sistema</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Criar grid de cards (3 colunas, com ajuste para 7 cards)
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7 = st.columns(1)[0]  # Para o sétimo card
    
    # Distribuir os cards
    with col1:
        criar_card(PLATAFORMAS[0])
    with col2:
        criar_card(PLATAFORMAS[1])
    with col3:
        criar_card(PLATAFORMAS[2])
    with col4:
        criar_card(PLATAFORMAS[3])
    with col5:
        criar_card(PLATAFORMAS[4])
    with col6:
        criar_card(PLATAFORMAS[5])
    with col7:
        criar_card(PLATAFORMAS[6])

def criar_card(plataforma):
    """Função auxiliar para criar cards de plataforma"""
    
    # CSS personalizado para o card
    st.markdown(f"""
        <div style='
            background-color: {plataforma.cor}15;
            border-radius: 20px;
            padding: 30px 20px;
            margin: 10px 0;
            text-align: center;
            border: 2px solid {plataforma.cor}30;
            transition: transform 0.3s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            height: 320px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        '>
            <div>
                <div style='
                    font-size: 4em;
                    margin-bottom: 20px;
                '>{plataforma.icone}</div>
                <h3 style='
                    color: {plataforma.cor};
                    margin-bottom: 10px;
                    font-size: 1.5em;
                '>{plataforma.nome}</h3>
                <p style='
                    color: #666;
                    margin-bottom: 20px;
                    font-size: 0.9em;
                '>{plataforma.descricao[:100]}{"..." if len(plataforma.descricao) > 100 else ""}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Botão para acessar a plataforma
    if st.button(f"Acessar {plataforma.nome}", key=f"btn_{plataforma.id}", use_container_width=True):
        st.session_state.plataforma_atual = plataforma.id
        st.session_state.pagina = "plataforma"
        st.rerun()

# ========== PÁGINA DA PLATAFORMA SELECIONADA ==========

def pagina_plataforma():
    """Página da plataforma selecionada"""
    
    # Encontrar a plataforma atual
    plataforma_atual = next((p for p in PLATAFORMAS if p.id == st.session_state.plataforma_atual), None)
    
    if not plataforma_atual:
        st.error("Plataforma não encontrada!")
        return
    
    # Header com navegação
    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col1:
        if st.button("← Voltar", type="secondary"):
            st.session_state.pagina = "dashboard"
            st.rerun()
    
    with col2:
        st.title(f"{plataforma_atual.icone} {plataforma_atual.nome}")
    
    with col3:
        st.write("")
    
    st.markdown("---")
    
    # Carregar o módulo da plataforma
    if plataforma_atual.modulo in MODULOS:
        MODULOS[plataforma_atual.modulo]()
    else:
        st.warning("Módulo em desenvolvimento...")

# ========== INICIALIZAÇÃO DO SISTEMA ==========

def main():
    """Função principal do sistema"""
    
    # Inicializar session state
    if 'gerenciador_usuarios' not in st.session_state:
        st.session_state.gerenciador_usuarios = GerenciadorUsuarios()
    
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "login"
    
    if 'usuario_logado' not in st.session_state:
        st.session_state.usuario_logado = None
    
    # Roteamento de páginas
    if not st.session_state.autenticado:
        if st.session_state.pagina == "cadastro":
            tela_cadastro()
        else:
            tela_login()
    else:
        if st.session_state.pagina == "plataforma":
            pagina_plataforma()
        else:
            dashboard_principal()

if __name__ == "__main__":
    main()