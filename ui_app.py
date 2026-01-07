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
# FUNÇÃO PADRÃO DE SUCESSO
# =========================
def sucesso():
    st.success("Salvo com sucesso!")

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background-image:
        linear-gradient(rgba(5, 30, 15, 0.88), rgba(5, 30, 15, 0.88)),
        url("https://images.unsplash.com/photo-1604014237744-1c46b84b7c67");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

h1 {
    text-align: center;
    font-weight: 800;
    color: #ffffff !important;
}

.subtitle {
    text-align: center;
    color: #ffffff;
    margin-bottom: 2rem;
    font-size: 0.95rem;
    letter-spacing: 1px;
}

label, label span {
    color: #ffffff !important;
    font-weight: 600;
}

div[data-testid="stVerticalBlock"] > div:has(form) {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.35);
    max-width: 760px;
    margin: auto;
}

input, textarea {
    color: #000000 !important;
}

div[data-baseweb="select"] span {
    color: #000000 !important;
}

/* SUCCESS EM BRANCO */
div[data-testid="stAlert"] p {
    color: #ffffff !important;
    font-weight: 800;
    text-align: center;
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
        clube_atleta = df_atletas.loc[df_atletas["Atleta"] == atleta, "Clube"].iloc[0]

        adversario = st.selectbox("🥊 Adversário", df_adversarios["Adversario"].tolist())
        clube_adv = df_adversarios.loc[
            df_adversarios["Adversario"] == adversario, "Clube"
        ].iloc[0]

        arenas = sorted(df_clubes["Arena"].dropna().unique().tolist())
        arena_padrao = df_clubes.loc[
            df_clubes["Clube"] == clube_atleta, "Arena"
        ].iloc[0]
        arena_index = arenas.index(arena_padrao) if arena_padrao in arenas else 0

        arena = st.selectbox("🏟️ Arena", arenas, index=arena_index)

        torneio = st.selectbox("🏆 Torneio", df_torneios["Torneio"].tolist())
        modalidade = st.selectbox("🎱 Modalidade", df_modalidade["Modalidade"].tolist())

        st.text_input("Clube Atleta", clube_atleta, disabled=True)
        st.text_input("Clube Adversário", clube_adv, disabled=True)

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
        sucesso()
        st.rerun()

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
        sucesso()
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
        sucesso()
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
        sucesso()
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
        sucesso()
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
        sucesso()
        st.rerun()
