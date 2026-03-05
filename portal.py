import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import json
import os
from dataclasses import dataclass
from typing import List, Optional
import time

# ====================== CONFIGURAÇÃO ======================
st.set_page_config(
    page_title="Portal de Plataformas",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== CLASSES ======================
@dataclass
class Usuario:
    id: str
    nome: str
    email: str
    senha_hash: str
    tipo: str
    plataformas_autorizadas: List[str]
    data_criacao: str
    ultimo_acesso: Optional[str] = None


class GerenciadorUsuarios:
    def __init__(self, arquivo="usuarios.json"):
        self.arquivo = arquivo
        self.carregar()
        if not self.usuarios:
            self.criar_admin_padrao()

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                self.usuarios = [Usuario(**u) for u in json.load(f)]
        else:
            self.usuarios = []

    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump([u.__dict__ for u in self.usuarios], f, indent=4, ensure_ascii=False)

    def criar_admin_padrao(self):
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
        self.salvar()

    def autenticar(self, email: str, senha: str) -> Optional[Usuario]:
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        for user in self.usuarios:
            if user.email == email and user.senha_hash == senha_hash:
                user.ultimo_acesso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.salvar()
                return user
        return None

    def criar_usuario(self, nome: str, email: str, senha: str, tipo: str, plataformas: List[str]):
        if any(u.email == email for u in self.usuarios):
            return False, "E-mail já cadastrado"
        novo = Usuario(
            id=f"USR{datetime.now().strftime('%Y%m%d%H%M%S')}",
            nome=nome,
            email=email,
            senha_hash=hashlib.sha256(senha.encode()).hexdigest(),
            tipo=tipo,
            plataformas_autorizadas=plataformas,
            data_criacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.usuarios.append(novo)
        self.salvar()
        return True, "Usuário criado com sucesso"


# ====================== PLATAFORMAS ======================
class Plataforma:
    def __init__(self, id: str, nome: str, icone: str, cor: str, descricao: str, modulo: str, link_externo: Optional[str] = None):
        self.id = id
        self.nome = nome
        self.icone = icone
        self.cor = cor
        self.descricao = descricao
        self.modulo = modulo
        self.link_externo = link_externo


PLATAFORMAS = [
    Plataforma("agendamento", "Sistema de Agendamento", "📅", "#FF4B4B", "Gerencie agendamentos, horários e serviços", "agendamento"),
    Plataforma("vendas", "Sistema de Vendas", "💰", "#00CC96", "Controle de vendas, estoque e clientes", "vendas"),
    Plataforma("financeiro", "Sistema Financeiro", "📊", "#FFA500", "Fluxo de caixa, contas a pagar/receber", "financeiro"),
    Plataforma("rh", "Sistema de RH", "👥", "#6C3483", "Gestão de funcionários e folha de pagamento", "rh"),
    Plataforma("estoque", "Sistema de Estoque", "📦", "#3498DB", "Controle de estoque e fornecedores", "estoque"),
    Plataforma("holerite", "Sistema de Holerite", "📄", "#27AE60",
               "Cálculos aproximados de 2026 (INSS e IRRF). Valide com contador.", "holerite_externo",
               link_externo="https://holeriteon-dlxxg3jqgtz25q9tf4wn7z.streamlit.app/"),
    Plataforma("relatorios", "Sistema de Relatórios", "📈", "#E74C3C", "Relatórios gerenciais e indicadores", "relatorios")
]


# ====================== MÓDULOS ======================
def modulo_agendamento():
    st.header("📅 Sistema de Agendamento")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Agendamentos Hoje", "12", "+2")
    with col2: st.metric("Agendamentos Semana", "45", "+5")
    with col3: st.metric("Taxa de Ocupação", "78%", "-3%")
    with col4: st.metric("Cancelamentos", "3", "-1")
    st.subheader("Próximos Agendamentos")
    dados = pd.DataFrame({
        "Cliente": ["João Silva", "Maria Santos", "Carlos Oliveira", "Ana Souza"],
        "Serviço": ["Corte", "Manicure", "Barba", "Coloração"],
        "Profissional": ["Carlos", "Ana", "João", "Maria"],
        "Data/Hora": ["14:30", "15:00", "15:30", "16:00"],
        "Status": ["Confirmado", "Confirmado", "Em espera", "Confirmado"]
    })
    st.dataframe(dados, use_container_width=True, hide_index=True)


def modulo_vendas():
    st.header("💰 Sistema de Vendas")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Vendas Hoje", "R$ 2.450", "+12%")
    with col2: st.metric("Vendas Mês", "R$ 45.890", "+8%")
    with col3: st.metric("Ticket Médio", "R$ 89,50", "+R$ 5,20")
    st.subheader("Últimas Vendas")
    dados = pd.DataFrame({
        "Cliente": ["Empresa A", "Empresa B", "Cliente C", "Cliente D"],
        "Produto": ["Produto X", "Serviço Y", "Produto Z", "Serviço W"],
        "Valor": ["R$ 1.200", "R$ 850", "R$ 320", "R$ 1.500"],
        "Data": ["10:30", "11:45", "14:20", "15:10"],
        "Status": ["Pago", "Pago", "Pendente", "Pago"]
    })
    st.dataframe(dados, use_container_width=True, hide_index=True)


def modulo_financeiro():
    st.header("📊 Sistema Financeiro")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Saldo Atual", "R$ 15.230", "+R$ 2.100")
    with col2: st.metric("Contas a Receber", "R$ 8.450", "+3")
    with col3: st.metric("Contas a Pagar", "R$ 4.320", "-2")
    with col4: st.metric("Fluxo Projetado", "R$ 19.360", "+12%")
    st.subheader("Fluxo de Caixa - Últimos 30 dias")
    dados = pd.DataFrame({
        "Dia": list(range(1, 11)),
        "Entradas": [1200, 1350, 1100, 1400, 1550, 1300, 1250, 1400, 1500, 1450],
        "Saídas": [800, 950, 700, 1100, 1050, 900, 850, 950, 1000, 1100]
    })
    st.line_chart(dados.set_index("Dia"))


def modulo_rh():
    st.header("👥 Sistema de RH")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Funcionários Ativos", "25", "+2")
    with col2: st.metric("Horas Trabalhadas", "3.450", "+120")
    with col3: st.metric("Afastamentos", "2", "-1")
    with col4: st.metric("Treinamentos", "3", "+1")
    st.subheader("Próximos Aniversários")
    dados = pd.DataFrame({
        "Funcionário": ["Ana Lima", "Carlos Sousa", "Mariana Silva"],
        "Cargo": ["Analista", "Coordenador", "Assistente"],
        "Data": ["15/05", "18/05", "22/05"],
        "Departamento": ["RH", "Vendas", "Financeiro"]
    })
    st.dataframe(dados, use_container_width=True, hide_index=True)


def modulo_estoque():
    st.header("📦 Sistema de Estoque")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total de Itens", "1.234", "+45")
    with col2: st.metric("Valor em Estoque", "R$ 45.670", "+R$ 3.200")
    with col3: st.metric("Itens em Falta", "8", "-3")
    with col4: st.metric("Pedidos Pendentes", "5", "+1")
    st.subheader("Produtos com Estoque Baixo")
    dados = pd.DataFrame({
        "Produto": ["Item A", "Item B", "Item C", "Item D"],
        "Quantidade": [5, 3, 2, 8],
        "Mínimo": [10, 10, 5, 15],
        "Fornecedor": ["Fornecedor X", "Fornecedor Y", "Fornecedor Z", "Fornecedor X"]
    })
    st.dataframe(dados, use_container_width=True, hide_index=True)


def modulo_holerite_externo():
    st.header("📄 Sistema de Holerite")
    plat = next(p for p in PLATAFORMAS if p.id == "holerite")
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #27AE60 0%, #219653 100%); padding: 50px; border-radius: 20px; 
                    text-align: center; color: white; margin: 30px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
            <div style='font-size: 5em; margin-bottom: 20px;'>📄</div>
            <h2 style='color:white; font-size:2.5em;'>Sistema de Holerite</h2>
            <p style='font-size:1.2em; max-width:600px; margin:0 auto 30px;'>
                Este é um sistema externo especializado em cálculos de holerite.
            </p>
            <div style='background:rgba(255,255,255,0.2); padding:15px; border-radius:10px; max-width:500px; margin:20px auto; font-size:0.95em;'>
                ⚠️ <strong>Aviso:</strong> Cálculos aproximados de 2026 (INSS/IRRF). Valide com contador.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.link_button("🌐 Abrir na mesma aba", plat.link_externo, use_container_width=True, type="primary")
        st.markdown(f"""
            <a href="{plat.link_externo}" target="_blank" style="text-decoration:none;">
                <div style='background:white; color:#27AE60; padding:12px; border-radius:10px; text-align:center;
                            font-weight:bold; border:2px solid #27AE60; margin:15px 0;'>
                    🔗 Abrir em Nova Aba
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("← Voltar ao Dashboard", use_container_width=True):
            st.session_state.pagina = "dashboard"
            st.rerun()


def modulo_relatorios():
    st.header("📈 Sistema de Relatórios")
    st.subheader("Relatórios Disponíveis")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Relatório de Vendas", use_container_width=True):
            st.info("Gerando relatório de vendas...")
            time.sleep(2)
            st.success("Relatório gerado!")
        if st.button("👥 Relatório de RH", use_container_width=True):
            st.info("Gerando relatório de RH...")
            time.sleep(2)
            st.success("Relatório gerado!")
        if st.button("📦 Relatório de Estoque", use_container_width=True):
            st.info("Gerando relatório de estoque...")
            time.sleep(2)
            st.success("Relatório gerado!")
    with col2:
        if st.button("💰 Relatório Financeiro", use_container_width=True):
            st.info("Gerando relatório financeiro...")
            time.sleep(2)
            st.success("Relatório gerado!")
        if st.button("📅 Relatório de Agendamentos", use_container_width=True):
            st.info("Gerando relatório de agendamentos...")
            time.sleep(2)
            st.success("Relatório gerado!")
        if st.button("📈 Relatório de Indicadores", use_container_width=True):
            st.info("Gerando relatório de indicadores...")
            time.sleep(2)
            st.success("Relatório gerado!")


MODULOS = {
    "agendamento": modulo_agendamento,
    "vendas": modulo_vendas,
    "financeiro": modulo_financeiro,
    "rh": modulo_rh,
    "estoque": modulo_estoque,
    "holerite_externo": modulo_holerite_externo,
    "relatorios": modulo_relatorios
}

# ====================== TELAS DE LOGIN/CADASTRO ======================
def tela_login():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .login-box { max-width:420px; margin:40px auto; padding:40px; background:white; border-radius:20px; box-shadow:0 15px 50px rgba(0,0,0,0.15); }
        </style>
    """, unsafe_allow_html=True)

    col = st.columns([1,2,1])[1]
    with col:
        st.markdown('<div class="login-box"><h1 style="text-align:center; color:#333;">🚀 Portal de Plataformas</h1>'
                    '<p style="text-align:center; color:#666;">Faça login para continuar</p></div>', unsafe_allow_html=True)
        
        with st.form("login"):
            email = st.text_input("📧 E-mail", placeholder="seu@email.com")
            senha = st.text_input("🔒 Senha", type="password")
            colb1, colb2 = st.columns(2)
            with colb1:
                if st.form_submit_button("Entrar", type="primary", use_container_width=True):
                    if email and senha:
                        user = st.session_state.gerenciador.autenticar(email, senha)
                        if user:
                            st.session_state.usuario_logado = user
                            st.session_state.autenticado = True
                            st.success("Login realizado!")
                            time.sleep(0.8)
                            st.rerun()
                        else:
                            st.error("E-mail ou senha inválidos")
                    else:
                        st.warning("Preencha os campos!")
            with colb2:
                if st.form_submit_button("Cadastrar", use_container_width=True):
                    st.session_state.pagina = "cadastro"
                    st.rerun()


def tela_cadastro():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .cadastro-box { max-width:420px; margin:40px auto; padding:40px; background:white; border-radius:20px; box-shadow:0 15px 50px rgba(0,0,0,0.15); }
        </style>
    """, unsafe_allow_html=True)

    col = st.columns([1,2,1])[1]
    with col:
        st.markdown('<div class="cadastro-box"><h1 style="text-align:center; color:#333;">📝 Cadastro de Usuário</h1></div>', unsafe_allow_html=True)
        
        with st.form("cadastro"):
            nome = st.text_input("👤 Nome completo", placeholder="Seu nome")
            email = st.text_input("📧 E-mail", placeholder="seu@email.com")
            senha = st.text_input("🔒 Senha", type="password")
            confirmar = st.text_input("🔒 Confirmar senha", type="password")
            colb1, colb2 = st.columns(2)
            with colb1:
                if st.form_submit_button("Cadastrar", type="primary", use_container_width=True):
                    if not all([nome, email, senha, confirmar]):
                        st.warning("Preencha todos os campos!")
                    elif senha != confirmar:
                        st.error("Senhas não conferem!")
                    else:
                        ok, msg = st.session_state.gerenciador.criar_usuario(nome, email, senha, "usuario", ["todas"])
                        if ok:
                            st.success(msg)
                            time.sleep(1.5)
                            st.session_state.pagina = "login"
                            st.rerun()
                        else:
                            st.error(msg)
            with colb2:
                if st.form_submit_button("Voltar ao Login", use_container_width=True):
                    st.session_state.pagina = "login"
                    st.rerun()

# ====================== DASHBOARD COM CARDS CLICÁVEIS ======================
def dashboard_principal():
    # Tratamento de query params para card clicado
    query_params = st.query_params.to_dict()
    if "plataforma" in query_params:
        plat_id = query_params["plataforma"][0]
        st.session_state.plataforma_atual = plat_id
        st.session_state.pagina = "plataforma"
        st.query_params.clear()
        st.rerun()

    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1: st.title(f"🚀 Bem-vindo, {st.session_state.usuario_logado.nome}!")
    with col2: st.write(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    with col3:
        if st.button("🚪 Sair", type="secondary"):
            st.session_state.clear()
            st.rerun()

    st.markdown("---")
    st.markdown("<h2 style='text-align:center;'>Escolha uma plataforma</h2><p style='text-align:center; color:#666;'>Você tem acesso a todas as 7 plataformas</p>", unsafe_allow_html=True)

    # CSS dos cards
    st.markdown("""
        <style>
        .platform-card {
            background-color: var(--bg);
            border: 2px solid var(--border);
            border-radius: 20px;
            padding: 30px 20px;
            margin: 12px 0;
            text-align: center;
            height: 340px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        }
        .platform-card:hover {
            transform: scale(1.04) translateY(-8px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        .platform-card .icone { font-size: 4.8em; margin-bottom: 15px; }
        .platform-card h3 { margin: 0 0 12px; font-size: 1.65em; }
        .platform-card p { color: #555; font-size: 0.97em; line-height: 1.45; }
        .acessar { color: var(--cor); font-weight: 700; font-size: 1.15em; margin-top: auto; }
        a.card-link { text-decoration: none; }
        </style>
    """, unsafe_allow_html=True)

    # Grid dinâmico
    num_cols = 3
    for i in range(0, len(PLATAFORMAS), num_cols):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            idx = i + j
            if idx < len(PLATAFORMAS):
                plat = PLATAFORMAS[idx]
                with cols[j]:
                    st.markdown(f"""
                        <a class="card-link" href="?plataforma={plat.id}">
                            <div class="platform-card" 
                                 style="--bg:{plat.cor}15; --border:{plat.cor}30; --cor:{plat.cor};">
                                <div>
                                    <div class="icone">{plat.icone}</div>
                                    <h3 style="color:{plat.cor};">{plat.nome}</h3>
                                    <p>{plat.descricao}</p>
                                </div>
                                <div class="acessar">→ Acessar plataforma</div>
                            </div>
                        </a>
                    """, unsafe_allow_html=True)

# ====================== PÁGINA DA PLATAFORMA ======================
def pagina_plataforma():
    plat = next((p for p in PLATAFORMAS if p.id == st.session_state.plataforma_atual), None)
    if not plat:
        st.error("Plataforma não encontrada")
        return

    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("← Voltar", type="secondary"):
            st.session_state.pagina = "dashboard"
            st.rerun()
    with col2:
        st.title(f"{plat.icone} {plat.nome}")

    st.markdown("---")
    if plat.modulo in MODULOS:
        MODULOS[plat.modulo]()
    else:
        st.warning("Módulo em desenvolvimento...")

# ====================== MAIN ======================
def main():
    if 'gerenciador' not in st.session_state:
        st.session_state.gerenciador = GerenciadorUsuarios()
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "login"
    if 'usuario_logado' not in st.session_state:
        st.session_state.usuario_logado = None

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