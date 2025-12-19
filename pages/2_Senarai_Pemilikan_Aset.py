import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Senarai Pemilikan Aset", layout="wide")

# =========================
# LOGO SIDEBAR (SAMA MACAM PAGE 1)
# =========================
logo_path = "cidb_logo.png"
st.sidebar.image(logo_path, width=140)



if st.sidebar.button("📊 Dashboard Aset Vs Easset", use_container_width=True):
    st.switch_page("Dashboard_Aset_Vs_Easset.py")   # tukar ikut nama file sebenar

if st.sidebar.button("📋 Senarai Pemilikan Aset", use_container_width=True):
    st.switch_page("pages/2_Senarai_Pemilikan_Aset.py")     # tukar ikut nama file sebenar

# =========================
# CSS (SAMA MACAM PAGE 1)
# =========================
css = """
<style>
/* PAGE BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #F9F6FF 0%, #FFFFFF 100%) !important;
    background-attachment: fixed !important;
}

/* SIDEBAR BACKGROUND */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #9B5CFF 0%, #7A3CFF 45%, #5A27E8 100%) !important;
    padding: 18px !important;
    border-right: none !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"] { display: none !important; }
section[data-testid="stSidebar"] [data-testid="stSidebarNavItems"] { display: none !important; }


/* Sidebar inner wrapper */
div[data-testid="stSidebarContent"] {
    background: transparent !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #FFFFFF !important;
}

/* Selectbox styling */
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border-radius: 12px !important;
}


section[data-testid="stSidebar"] div[data-baseweb="select"] div,
section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #555555 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #555555 !important;
}


/* HIDE DEFAULT STREAMLIT MULTIPAGE NAV (yang ada 2 link tu) */
section[data-testid="stSidebar"] nav {
    display: none !important;
}

/* TABLE STYLE */
table {
    border-collapse: collapse;
    width: 100%;
    font-size: 15px;
}
thead tr th {
    background-color: #E8D7FF !important;
    color: #4B3F72 !important;
    font-weight: 700 !important;
    text-align: left !important;
    padding: 10px !important;
    border-bottom: 2px solid #D3B6FF !important;
    position: sticky;
    top: 0;
    z-index: 2;
}
tbody tr td {
    padding: 8px 10px !important;
    border-bottom: 1px solid #F0E6FF !important;
    color: #333 !important;
}
tbody tr:hover td {
    background-color: #F6EEFF !important;
}
tbody tr:nth-child(even) {
    background-color: #ffffff !important;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)



# =========================
# SELECTBOX MAIN PAGE – DROPDOWN HOVER (NO GREY)
# =========================
st.markdown("""
<style>
/* dropdown container */
div[data-baseweb="popover"]{
    border-radius: 14px !important;
    box-shadow: 0 12px 30px rgba(90,39,232,0.18) !important;
}

/* option item */
div[data-baseweb="menu"] li{
    font-size: 14px !important;
    padding: 10px 14px !important;
    color: #3f3f3f !important;
}

/* hover → purple cerah */
div[data-baseweb="menu"] li:hover{
    background: rgba(176,145,255,0.22) !important;
    color: #2d1b5a !important;
}

/* selected */
div[data-baseweb="menu"] li[aria-selected="true"]{
    background: rgba(176,145,255,0.35) !important;
    font-weight: 700 !important;
    color: #2d1b5a !important;
}

/* keyboard focus */
div[data-baseweb="menu"] li:focus{
    background: rgba(176,145,255,0.28) !important;
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* =========================
   MAIN PAGE SELECTBOX (Nama Pegawai)
   ========================= */
div[data-testid="stSelectbox"] > label {
    font-weight: 700 !important;
    color: #6b6b6b !important;
}

/* kotak select utama */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: rgba(176,145,255,0.14) !important;      /* purple cerah */
    border: 1px solid rgba(122,60,255,0.55) !important;  /* outline purple */
    border-radius: 14px !important;
    box-shadow: 0 8px 18px rgba(90,39,232,0.10) !important;
}

/* hover */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {
    border-color: rgba(122,60,255,0.85) !important;
}

/* focus (klik) */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within{
    border-color: rgba(122,60,255,0.95) !important;
    box-shadow: 0 0 0 3px rgba(176,145,255,0.35) !important;
}



/* =========================
   DOWNLOAD BUTTON (Download CSV)
   ========================= */
div[data-testid="stDownloadButton"] button{
    background: rgba(176,145,255,0.75) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.55) !important;
    border-radius: 14px !important;
    padding: 10px 16px !important;
    font-weight: 800 !important;
    box-shadow: 0 8px 18px rgba(90,39,232,0.20) !important;
    transition: all 0.2s ease;
}

div[data-testid="stDownloadButton"] button:hover{
    background: rgba(90,39,232,0.55) !important;
    border-color: rgba(255,255,255,0.75) !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* BORDERLESS CARD for st.container(border=True) */
div[data-testid="stVerticalBlockBorderWrapper"]{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div{
    background: #FFFFFF !important;
    border: none !important;
    border-radius: 18px !important;
    overflow: hidden !important;
    box-shadow:
        0 10px 28px rgba(155, 92, 255, 0.18),
        0 2px 6px rgba(155, 92, 255, 0.10) !important;
    padding: 20px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ===============================
   SIDEBAR FIX (SAMA PAGE 1)
   =============================== */

/* hide collapse << */
button[data-testid="collapsedControl"]{
    display: none !important;
}

/* sidebar container */
section[data-testid="stSidebar"]{
    overflow: hidden !important;
}

/* scroll content */
div[data-testid="stSidebarContent"]{
    overflow-y: auto !important;
    padding-right: 8px !important;   /* bagi ruang scrollbar supaya tak terkepit */
    box-sizing: border-box !important;
}

/* scrollbar cantik */
div[data-testid="stSidebarContent"]::-webkit-scrollbar{
    width: 6px;
}
div[data-testid="stSidebarContent"]::-webkit-scrollbar-thumb{
    background: rgba(255,255,255,0.35);
    border-radius: 10px;
}
div[data-testid="stSidebarContent"]::-webkit-scrollbar-track{
    background: transparent;
}

/* ===============================
   NAV BUTTON (SAMA PAGE 1)
   =============================== */
section[data-testid="stSidebar"] button[kind="secondary"]{
    background: rgba(255,255,255,0.18) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.28) !important;
    border-radius: 14px !important;

    padding: 12px 14px !important;
    font-size: 14px !important;
    font-weight: 700 !important;

    text-align: left !important;
    width: calc(100% - 4px) !important;
    box-sizing: border-box !important;
}

section[data-testid="stSidebar"] button[kind="secondary"]:hover{
    background: rgba(255,255,255,0.30) !important;
    border-color: rgba(255,255,255,0.40) !important;
}

/* OPTIONAL: highlight "selected" utk PAGE 2 (button ke-2) */
section[data-testid="stSidebar"]
div[data-testid="stSidebarContent"]
button[kind="secondary"]:nth-of-type(2){
    background: rgba(255,255,255,0.32) !important;
    border-color: rgba(255,255,255,0.55) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# GOOGLE DRIVE HELPERS
# =========================
def _download_gdrive_file(file_id: str) -> bytes:
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()

    r = session.get(URL, params={"id": file_id}, stream=True)
    r.raise_for_status()

    token = None
    for k, v in r.cookies.items():
        if k.startswith("download_warning"):
            token = v
            break

    if token:
        r = session.get(URL, params={"id": file_id, "confirm": token}, stream=True)
        r.raise_for_status()

    return r.content


def read_csv_from_gdrive(file_id: str, **read_csv_kwargs) -> pd.DataFrame:
    content = _download_gdrive_file(file_id)
    return pd.read_csv(io.BytesIO(content), **read_csv_kwargs)

def load_easset_once():
    if "df_easset_raw" not in st.session_state:
        st.session_state["df_easset_raw"] = read_csv_from_gdrive(EASSET_FILE_ID)

    return st.session_state["df_easset_raw"].copy()


# =========================
# FILE PATHS (SAMA PROJECT)
# =========================
EASSET_FILE_ID = "1JDjlKqqBUF1k0ET9YiBHPf0T5cu4ihhs"
DIM_EVA_PATH   = "DIM Eva grp 1.csv"


# =========================
# LOAD DATA (EASSET SAHAJA)
# =========================
df_easset = load_easset_once()
dim_eva = pd.read_csv(DIM_EVA_PATH)

df_easset.columns = df_easset.columns.str.strip()
dim_eva.columns = dim_eva.columns.str.strip()

# =========================
# CLEAN DIM EVA (untuk PTJ full form)
# =========================
dim_eva = dim_eva.rename(columns={
    "Eval. Grp 1-Block": "eva_grp1",
    "Eval. Grp 1": "eva_grp1",
    "Detail": "eva_desc",
    "Detail 2": "eva_detail2",
    "Detail 3": "eva_detail3",
})
dim_eva["eva_grp1"] = dim_eva["eva_grp1"].astype(str).str.strip()

eva_desc_map    = dim_eva.set_index("eva_grp1")["eva_desc"].to_dict()
eva_detail2_map = dim_eva.set_index("eva_grp1")["eva_detail2"].to_dict()
eva_detail3_map = dim_eva.set_index("eva_grp1")["eva_detail3"].to_dict()
ptj_full_map = {
    "HQ": "HQ",
    "BT": "Bintulu",
    "JH": "Johor",
    "KD": "Kedah",
    "KN": "Kelantan",
    "ML": "Melaka",
    "NS": "Negeri Sembilan",
    "PP": "Penang",
    "PH": "Pahang",
    "PR": "Perak",
    "PL": "Perlis",
    "SB": "Sabah",
    "SR": "Sarawak",
    "SL": "Selangor",
    "TR": "Terengganu",
    "TW": "Tawau",
    "WPKL": "W.P Kuala Lumpur",
    "SI": "Sibu",
    "SD": "Sandakan",
    "MR": "Miri",
}


# =========================
# CLEAN EASSET
# =========================
df_easset = df_easset.rename(columns={
    "No. Aset SAP": "asset_no",
    "Sub Aset SAP": "sub_no",
    "Jenama": "description",
    "Pegawai Penempatan": "officer",
    "Eval Group 1": "eva_grp1",
})
df_easset["asset_no"] = pd.to_numeric(df_easset["asset_no"], errors="coerce").fillna(0).astype(int)
df_easset["sub_no"] = pd.to_numeric(df_easset["sub_no"], errors="coerce").fillna(0).astype(int)
df_easset["eva_grp1"] = df_easset["eva_grp1"].astype(str).str.strip()

# Map EVA → Lokasi
df_easset["Lokasi (Full)"] = df_easset["eva_grp1"].map(eva_detail2_map)
df_easset["Lokasi (Ringkas)"] = df_easset["eva_grp1"].map(eva_desc_map)

df_easset["Lokasi (Full)"] = (
    df_easset["Lokasi (Full)"]
    .fillna(df_easset["Lokasi (Ringkas)"])
    .fillna("Tidak Diketahui")
)

df_easset["PTJ_Display"] = df_easset["Lokasi (Full)"].map(ptj_full_map).fillna(df_easset["Lokasi (Full)"])


# Bahagian (guna DIM PTJ column "Detail")
df_easset["Bahagian"] = df_easset["eva_grp1"].map(eva_desc_map)

# Bahagian hanya untuk Ibu Pejabat
df_easset.loc[
    df_easset["Lokasi (Full)"] != "HQ",
    "Bahagian"
] = pd.NA


# =========================
# DERIVE ASSET CLASS (SAMA LOGIC PAGE 1)
# =========================
valid_prefix = ["30","40","41","50","51","52","53","54","60","61","70","80","81"]

df_easset["prefix"] = df_easset["asset_no"].astype(str).str[:2]
df_easset = df_easset[df_easset["prefix"].isin(valid_prefix)]

df_easset["asset_class"] = df_easset["prefix"].astype(int) * 1000

allowed_asset_classes = [
    30000, 40000, 41000,
    50000, 51000, 52000, 53000, 54000,
    60000, 61000,
    70000,
    80000, 81000
]

df_easset = df_easset[df_easset["asset_class"].isin(allowed_asset_classes)].copy()



# =========================
# BASE DATA (UNTUK CASCADING FILTER)
# =========================
df_base = df_easset.copy()


df_base["officer"] = df_base["officer"].astype(str).str.strip()
df_base.loc[df_base["officer"].isin(["", "nan", "None"]), "officer"] = pd.NA

st.title("Senarai Pemilikan Aset (Easset)")

# =========================
# FILTER SECTION
# =========================
st.sidebar.title("Tapisan")

# 1️⃣ PTJ (FILTER FIRST)
ptj_list = sorted(df_base["PTJ_Display"].dropna().unique().tolist())
ptj_list.insert(0, "Semua")

ptj_filter = st.sidebar.selectbox("PTJ (Easset)", ptj_list)

if ptj_filter != "Semua":
    df_after_ptj = df_base[df_base["PTJ_Display"] == ptj_filter].copy()

else:
    df_after_ptj = df_base.copy()

# 2️⃣ BAHAGIAN (ONLY IF PTJ = HQ)
bahagian_filter = "Semua"
df_after_bahagian = df_after_ptj

if ptj_filter == "HQ":
    bahagian_list = sorted(df_after_ptj["Bahagian"].dropna().unique().tolist())
    bahagian_list.insert(0, "Semua")

    bahagian_filter = st.sidebar.selectbox("Bahagian", bahagian_list)

    if bahagian_filter != "Semua":
        df_after_bahagian = df_after_ptj[df_after_ptj["Bahagian"] == bahagian_filter].copy()


# 3️⃣ NAMA PEGAWAI (BASED ON PTJ + BAHAGIAN)
pegawai_list = sorted(df_after_bahagian["officer"].dropna().unique().tolist())
pegawai_list.insert(0, "Semua")

nama_pegawai = st.selectbox("Nama Pegawai", pegawai_list)

if nama_pegawai != "Semua":
    df_view = df_after_bahagian[df_after_bahagian["officer"] == nama_pegawai].copy()
else:
    df_view = df_after_bahagian.copy()



# =========================
# HEADER + DOWNLOAD
# =========================


title_col, btn_col = st.columns([8, 2], vertical_alignment="center")

with title_col:
    st.markdown(
        "<h2 style='font-size:24px; font-weight:700; color:#8c92ac;'>"
        "Senarai penuh aset dalam Easset"
        "</h2>",
        unsafe_allow_html=True
    )

with btn_col:
    csv_data = df_view.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv_data,
        file_name="senarai_pemilikan_aset_easset.csv",
        mime="text/csv",
        use_container_width=True
    )

# =========================
# TABLE (SHOW ONLY WHEN FILTERED)
# =========================
is_filtered = (ptj_filter != "Semua") or (bahagian_filter != "Semua") or (nama_pegawai != "Semua")

if not is_filtered:
    st.info("Sila pilih **PTJ** atau **Nama Pegawai** untuk papar jadual")
else:
    # only show light columns
    df_table = df_view.loc[:, ["asset_no", "sub_no", "description", "officer"]].copy()

    df_table = df_table.rename(columns={
        "asset_no": "Asset No",
        "sub_no": "Sub No",
        "description": "Description",
        "officer": "Nama Pegawai"
    })

    df_table = df_table.reset_index(drop=True)
    df_table.insert(0, "Bil", range(1, len(df_table) + 1))

    table_html = df_table.to_html(index=False)

    st.markdown(
        f"""
        <div style="
            max-height: 520px;
            overflow-y: auto;
            border-radius: 10px;
            border: 1px solid #F0E6FF;
            box-shadow: 0 4px 10px rgba(150, 80, 255, 0.07);
            margin-top: 8px;
        ">
            {table_html}
        </div>
        """,
        unsafe_allow_html=True
    )
