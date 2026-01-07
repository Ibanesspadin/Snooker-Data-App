import pandas as pd
from sheets import connect_sheet

NOME_PLANILHA = "Snooker_BI_Oficial"

# =========================
# CONEXÃO / WORKSHEET
# =========================
def get_worksheet(nome_aba):
    client = connect_sheet()
    spreadsheet = client.open(NOME_PLANILHA)
    return spreadsheet.worksheet(nome_aba)

# =========================
# DIMENSÕES - GET
# =========================
def get_dim_atletas():
    sheet = get_worksheet("DIM_ATLETAS")
    return pd.DataFrame(sheet.get_all_records())

def get_dim_adversarios():
    sheet = get_worksheet("DIM_ADVERSARIOS")
    return pd.DataFrame(sheet.get_all_records())

def get_dim_clubes():
    sheet = get_worksheet("DIM_CLUBES")
    return pd.DataFrame(sheet.get_all_records())

def get_dim_torneios():
    sheet = get_worksheet("DIM_TORNEIOS")
    return pd.DataFrame(sheet.get_all_records())

def get_dim_modalidade():
    sheet = get_worksheet("DIM_MODALIDADE")
    return pd.DataFrame(sheet.get_all_records())

# =========================
# FAT - INSERT
# =========================
def insert_fat_partida(linha):
    sheet = get_worksheet("FAT_PARTIDAS")
    sheet.append_row(linha)

# =========================
# BUSCAS AUXILIARES
# =========================
def get_clube_by_atleta(nome_atleta):
    df = get_dim_atletas()
    row = df[df["Atleta"] == nome_atleta]
    return row.iloc[0]["Clube"] if not row.empty else ""

def get_clube_by_adversario(nome_adversario):
    df = get_dim_adversarios()
    row = df[df["Adversario"] == nome_adversario]
    return row.iloc[0]["Clube"] if not row.empty else ""

def get_arena_by_clube(clube):
    df = get_dim_clubes()
    row = df[df["Clube"] == clube]
    return row.iloc[0]["Arena"] if not row.empty else ""

# =========================
# DIMENSÕES - INSERT
# =========================
def insert_dim_atleta(
    atleta,
    clube,
    tempo_jogo_anos="",
    taco_marca="",
    taco_modelo="",
    taco_tamanho="",
    taco_sola="",
    maior_six="",
    maior_rb=""
):
    sheet = get_worksheet("DIM_ATLETAS")
    sheet.append_row([
        atleta,
        clube,
        tempo_jogo_anos,
        taco_marca,
        taco_modelo,
        taco_tamanho,
        taco_sola,
        maior_six,
        maior_rb,
        ""
    ])

def insert_dim_adversario(adversario, apelido, clube):
    sheet = get_worksheet("DIM_ADVERSARIOS")
    sheet.append_row([adversario, apelido, clube])

def insert_dim_clube(clube, arena, cidade, estado, tipo):
    sheet = get_worksheet("DIM_CLUBES")
    sheet.append_row([clube, arena, cidade, estado, tipo])

def insert_dim_torneio(torneio, tipo, modalidade):
    sheet = get_worksheet("DIM_TORNEIOS")
    sheet.append_row([torneio, tipo, modalidade])

def insert_dim_modalidade(modalidade):
    sheet = get_worksheet("DIM_MODALIDADE")
    sheet.append_row([modalidade])
