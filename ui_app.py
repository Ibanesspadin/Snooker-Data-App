import streamlit as st
from datetime import date
from repository import (
    get_dim_atletas,
    get_dim_adversarios,
    get_dim_clubes,
    get_dim_torneios,
    get_dim_modalidade,
    insert_fat_partida,
    insert_dim_atleta,
    insert_dim_adversario,
    insert_dim_clube,
    insert_dim_torneio,
    insert_dim_modalidade
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Snooker Data App",
    page_icon="🎱",
    layout="centered"
)

# =========================
# CSS GLOBAL
# =========================
st.markdown("""
<style>
/* FUNDO */
.stApp {
    background-image:
        linear-gradient(rgba(5, 30, 15, 0.88), rgba(5, 30, 15, 0.88)),
        url("https://images.unsplash.com/photo-1604014237744-1c46b84b7c67");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* TÍTULO */
h1 {
    text-align: center;
    font-weight: 800;
    color: #ffffff !important;
}

/* SUBTÍTULO */
.subtitle {
    text-align: center;
    color: #ffffff;
    margin-bottom: 2rem;
    font-size: 0.95rem;
    letter-spacing: 1px;
}

/* LABELS */
label, label span {
    color: #ffffff !important;
    font-weight: 600;
}

/* CARD */
div[data-testid="stVerticalBlock"] > div:has(form) {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.35);
    max-width: 760px;
    margin: auto;
}

/* INPUTS */
input, textarea {
    color: #000000 !important;
}

div[data-baseweb="select"] span {
    color: #000000 !important;
}

/* =========================
   TABS — TODAS BRANCAS
========================= */
button[data-baseweb="tab"] {
    color: #ffffff !important;
    font-weight: 600;
    opacity: 1 !important;
    background-color: transparent !important;
}

/* TAB ATIVA */
button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
    font-weight: 800;
    border-bottom: 3px solid #d90429 !important;
}

/* HOVER */
button[data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background-color: transparent !important;
}

/* BOTÃO SALVAR */
button[kind="primary"],
button[kind="primary"]:hover,
button[kind="primary"]:active,
button[kind="primary"]:focus {
    background-color: #0f5132 !important;
    color: #ffffff !important;
    border-radius: 12px;
    padding: 0.8rem 1.6rem;
    font-weight: 800;
    border: none !important;
    width: 100%;
    margin-top: 1.5rem;
    box-shadow: 0 6px 18px rgba(0,0,0,0.45);
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🎱 Snooker Data App")
st.markdown(
    "<div class='subtitle'>Sistema de cadastro de partidas, atletas, clubes e torneios</div>",
    unsafe_allow_html=True
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_dims():
    return (
        get_dim_atletas(),
        get_dim_adversarios(),
        get_dim_clubes(),
        get_dim_torneios(),
        get_dim_modalidade()
    )

df_atletas, df_adversarios, df_clubes, df_torneios, df_modalidade = load_dims()

# =========================
# TABS
# =========================
tab_partida, tab_adv, tab_atleta, tab_torneio, tab_clube, tab_modalidade = st.tabs([
    "🎱 Nova Partida",
    "🥊 Novo Adversário",
    "🎯 Novo Atleta",
    "🏆 Novo Torneio",
    "🏟️ Novo Clube",
    "🎱 Nova Modalidade"
])

# =========================
# 🎱 PARTIDA
# =========================
with tab_partida:
    with st.form("form_partida"):
        data = st.date_input("📅 Data da Partida", value=date.today())

        atleta = st.selectbox("🎱 Atleta", df_atletas["Atleta"].tolist())
        clube_atleta = df_atletas.loc[df_atletas["Atleta"] == atleta, "Clube"]_]()
