import streamlit as st
from datetime import date
from repository import (
    get_dim_atletas,
    get_dim_adversarios,
    get_dim_clubes,
    get_dim_torneios,
    get_dim_modalidade,
    get_clube_by_atleta,
    get_clube_by_adversario,
    get_arena_by_clube,
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
# CSS FINAL – BOTÃO FIXO
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
    padding: 2rem 2rem 2.5rem 2rem;
    border-radius: 16px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.35);
    max-width: 760px;
    margin: auto;
}

/* INPUTS */
input, textarea {
    color: #000000 !important;
}

/* SELECT */
div[data-baseweb="select"] span {
    color: #000000 !important;
}

/* INPUT DESABILITADO */
input:disabled {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    opacity: 1 !important;
}

/* =========================
   BOTÃO FIXO – SEM HOVER
========================= */
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
    transform: none !important;
    outline: none !important;
}

/* TABS */
button[data-baseweb="tab"] {
    color: #ffffff !important;
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    border-bottom: 3px solid #d90429 !important;
    font-weight: 800;
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
# LOAD DIMS
# =========================
df_atletas = get_dim_atletas()
df_adversarios = get_dim_adversarios()
df_clubes = get_dim_clubes()
df_torneios = get_dim_torneios()
df_modalidade = get_dim_modalidade()

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
        clube_atleta = get_clube_by_atleta(atleta)

        adversario = st.selectbox("🥊 Adversário", df_adversarios["Adversario"].tolist())
        clube_adv = get_clube_by_adversario(adversario)

        arena = get_arena_by_clube(clube_atleta)
        torneio = st.selectbox("🏆 Torneio", df_torneios["Torneio"].tolist())
        modalidade = st.selectbox("🎱 Modalidade", df_modalidade["Modalidade"].tolist())

        st.text_input("Clube Atleta", clube_atleta, disabled=True)
        st.text_input("Clube Adversário", clube_adv, disabled=True)
        st.text_input("Arena", arena, disabled=True)

        placar_atleta = st.number_input("Placar Atleta", min_value=0)
        placar_adv = st.number_input("Placar Adversário", min_value=0)
        maior_tacada = st.number_input("🔥 Maior Tacada", min_value=0)

        salvar = st.form_submit_button("💾 SALVAR PARTIDA")

    if salvar:
        insert_fat_partida([
            data.strftime("%d/%m/%Y"),
            atleta,
            adversario,
            clube_atleta,
            clube_adv,
            arena,
            torneio,
            data.year,
            placar_atleta,
            placar_adv,
            maior_tacada,
            modalidade
        ])
        st.success("🎉 Partida registrada com sucesso!")

# =========================
# 🥊 ADVERSÁRIO
# =========================
with tab_adv:
    with st.form("form_adv"):
        nome = st.text_input("Nome do Adversário")
        apelido = st.text_input("Apelido")
        clube = st.selectbox("Clube", df_clubes["Clube"].tolist())
        salvar = st.form_submit_button("💾 SALVAR ADVERSÁRIO")

    if salvar:
        insert_dim_adversario(nome, apelido, clube)
        st.success("✅ Adversário cadastrado")
        st.rerun()

# =========================
# 🎯 ATLETA
# =========================
with tab_atleta:
    with st.form("form_atleta"):
        nome = st.text_input("Nome do Atleta")
        clube = st.selectbox("Clube", df_clubes["Clube"].tolist())
        tempo = st.number_input("Tempo de Jogo (anos)", min_value=0)
        marca = st.text_input("Marca do Taco")
        modelo = st.text_input("Modelo do Taco")
        tamanho = st.text_input("Tamanho do Taco")
        sola = st.text_input("Sola do Taco")
        six = st.number_input("Maior Tacada Six Red's", min_value=0)
        rb = st.number_input("Maior Tacada Regra Brasileira", min_value=0)
        salvar = st.form_submit_button("💾 SALVAR ATLETA")

    if salvar:
        insert_dim_atleta(nome, clube, tempo, marca, modelo, tamanho, sola, six, rb)
        st.success("✅ Atleta cadastrado")
        st.rerun()

# =========================
# 🏆 TORNEIO
# =========================
with tab_torneio:
    with st.form("form_torneio"):
        nome = st.text_input("Nome do Torneio")
        tipo = st.text_input("Tipo")
        modalidade = st.selectbox("Modalidade", df_modalidade["Modalidade"].tolist())
        salvar = st.form_submit_button("💾 SALVAR TORNEIO")

    if salvar:
        insert_dim_torneio(nome, tipo, modalidade)
        st.success("✅ Torneio cadastrado")
        st.rerun()

# =========================
# 🏟️ CLUBE
# =========================
with tab_clube:
    with st.form("form_clube"):
        nome = st.text_input("Nome do Clube")
        arena = st.text_input("Arena")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")
        tipo = st.text_input("Tipo")
        salvar = st.form_submit_button("💾 SALVAR CLUBE")

    if salvar:
        insert_dim_clube(nome, arena, cidade, estado, tipo)
        st.success("✅ Clube cadastrado")
        st.rerun()

# =========================
# 🎱 MODALIDADE
# =========================
with tab_modalidade:
    with st.form("form_modalidade"):
        nome = st.text_input("Nome da Modalidade")
        salvar = st.form_submit_button("💾 SALVAR MODALIDADE")

    if salvar:
        insert_dim_modalidade(nome)
        st.success("✅ Modalidade cadastrada")
        st.rerun()
