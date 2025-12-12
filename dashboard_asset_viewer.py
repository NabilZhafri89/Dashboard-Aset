import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(page_title="Dashboard SAP Vs Easset", layout="wide")

# =========================
# LOGO SIDEBAR
# =========================
logo_path = "cidb_logo.png"

# Tarik balik jarak supaya "Tapisan" tak jauh ke bawah
st.sidebar.markdown("<div style='margin-top:-15px;'></div>", unsafe_allow_html=True)

# =========================
# CSS (PAGE + SIDEBAR + TABLE + KPI)
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
    padding: 18px !important;  /* reduce padding to avoid sidebar scroll */
    border-right: none !important;
}

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

/* KPI CARD */
.kpi-card {
    background: #D9C8FF;
    border-radius: 18px;
    padding: 18px 22px;
    height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 10px 28px rgba(150, 80, 255, 0.20);
}
.kpi-title {
    font-size: 16px;
    font-weight: 600;
    color: #8E79BB;
}
.kpi-number {
    font-size: 40px;
    font-weight: 800;
    color: #FFFFFF;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

st.markdown("""
<style>
/* ==============================
   CHART CARD (borderless + shadow)
   ============================== */
div[data-testid="stPlotlyChart"]{
    background: #FFFFFF !important;
    border: none !important;
    border-radius: 18px !important;

    box-shadow:
        0 10px 28px rgba(155, 92, 255, 0.18),
        0 2px 6px rgba(155, 92, 255, 0.10) !important;

    padding: 20px !important;
    margin-top: 12px !important;
}

/* pastikan clip ikut border radius */
div[data-testid="stPlotlyChart"] > div{
    border-radius: 18px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)



# =========================
# KPI CARD FUNCTION
# =========================
def kpi_card(title, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-number">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# FILE PATHS
# =========================
SAP_PATH = "Asset_Balance_SAP.csv"
EASSET_PATH = "Senarai_Aset_Easset.csv"
DIM_CLASS_PATH = "DIM Asset Class.csv"
DIM_EVA_PATH = "DIM Eva grp 1.csv"

# Tarikh kemaskini
last_update_timestamp = os.path.getmtime(SAP_PATH)
last_update_date = datetime.fromtimestamp(last_update_timestamp).strftime("%d %b %Y")

# =========================
# LOAD DATA
# =========================
df_sap = pd.read_csv(SAP_PATH)
df_easset = pd.read_csv(EASSET_PATH)
dim_class = pd.read_csv(DIM_CLASS_PATH)
dim_eva = pd.read_csv(DIM_EVA_PATH)

df_sap.columns = df_sap.columns.str.strip()
df_easset.columns = df_easset.columns.str.strip()
dim_class.columns = dim_class.columns.str.strip()
dim_eva.columns = dim_eva.columns.str.strip()

# =========================
# DIM CLEAN
# =========================
dim_class = dim_class.rename(columns={
    "Asset Class": "asset_class",
    "Asset Clas": "asset_class",
    "Detail": "asset_class_desc"
})
dim_class["asset_class"] = dim_class["asset_class"].astype(int)

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

def enrich_with_eva_details(df, code_col, prefix):
    if code_col not in df.columns:
        return df
    codes = df[code_col].astype(str).str.strip()
    df[f"{prefix}_eva_desc"]    = codes.map(eva_desc_map)
    df[f"{prefix}_eva_detail2"] = codes.map(eva_detail2_map)
    df[f"{prefix}_eva_detail3"] = codes.map(eva_detail3_map)
    return df

def add_kategori_aset(df):
    if "asset_class_sap" in df.columns:
        effective = df["asset_class_sap"]
        if "asset_class_easset" in df.columns:
            effective = effective.fillna(df["asset_class_easset"])
    elif "asset_class_easset" in df.columns:
        effective = df["asset_class_easset"]
    elif "asset_class" in df.columns:
        effective = df["asset_class"]
    else:
        return df

    effective = pd.to_numeric(effective, errors="coerce")

    def classify(x):
        if pd.isna(x):
            return None
        if x in [81000, 82000]:
            return "Aset Tak Ketara"
        return "Aset Alih"

    df["kategori_aset"] = effective.apply(classify)
    return df

def add_ptj_slicer_col(df):
    ptj = None
    if "sap_eva_detail3" in df.columns:
        ptj = df["sap_eva_detail3"]
    if "easset_eva_detail3" in df.columns:
        if ptj is None:
            ptj = df["easset_eva_detail3"]
        else:
            ptj = ptj.fillna(df["easset_eva_detail3"])
    if ptj is not None:
        df["ptj_slicer_col"] = ptj
    return df

# =========================
# CLEAN SAP
# =========================
df_sap = df_sap.rename(columns={
    "Asset Class": "asset_class",
    "Asset Clas": "asset_class",
    "Asset": "asset_no",
    "Sub-number": "sub_no",
    "Sub-numb": "sub_no",
    "Eval. Grp 1-Block": "eva_grp1",
    "Eval. Grp 1": "eva_grp1",
    "Asset Description": "description",
    "Acquis.val.": "acquisition_value",
    "Book val.": "book_value",
})

df_sap = df_sap[df_sap["asset_no"].notna()]
df_sap = df_sap[df_sap["asset_no"].astype(str).str.strip() != ""]

df_sap["asset_no"] = pd.to_numeric(df_sap["asset_no"], errors="coerce")
df_sap = df_sap[df_sap["asset_no"].notna()]
df_sap["asset_no"] = df_sap["asset_no"].astype(int)

df_sap["sub_no"] = pd.to_numeric(df_sap["sub_no"], errors="coerce").fillna(0).astype(int)
df_sap["asset_class"] = pd.to_numeric(df_sap["asset_class"], errors="coerce").fillna(0).astype(int)
df_sap["eva_grp1"] = df_sap["eva_grp1"].astype(str).str.strip()

df_sap["acquisition_value"] = pd.to_numeric(df_sap["acquisition_value"], errors="coerce").fillna(0)

misclassified_low_value = df_sap[
    (df_sap["asset_class"].isin([40000, 41000])) &
    (df_sap["acquisition_value"] < 2000)
].copy()
misclassified_low_value["Misclassification Issue"] = "Nilai < RM2000 tetapi dalam kelas 40000/41000"
misclassified_low_value = enrich_with_eva_details(misclassified_low_value, "eva_grp1", "sap")
misclassified_low_value = add_kategori_aset(misclassified_low_value)
misclassified_low_value = add_ptj_slicer_col(misclassified_low_value)

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

valid_prefix = ["30","40","41","50","51","52","53","54","60","61","70","80","81","82"]
df_easset["prefix"] = df_easset["asset_no"].astype(str).str[:2]
df_easset = df_easset[df_easset["prefix"].isin(valid_prefix)]
df_easset["asset_class"] = df_easset["prefix"].astype(int) * 1000

# =========================
# RECONCILIATION
# =========================
recon = df_sap.merge(
    df_easset,
    on=["asset_no", "sub_no"],
    how="outer",
    indicator=True,
    suffixes=("_sap", "_easset")
)

sap_only = recon[recon["_merge"] == "left_only"].copy()
easset_only = recon[recon["_merge"] == "right_only"].copy()

both = recon[recon["_merge"] == "both"].copy()
both["eva_grp1_sap"] = both["eva_grp1_sap"].astype(str).str.strip()
both["eva_grp1_easset"] = both["eva_grp1_easset"].astype(str).str.strip()
diff_eva = both[both["eva_grp1_sap"].fillna("") != both["eva_grp1_easset"].fillna("")].copy()

sap_only = enrich_with_eva_details(sap_only, "eva_grp1_sap", "sap")
sap_only = enrich_with_eva_details(sap_only, "eva_grp1_easset", "easset")

easset_only = enrich_with_eva_details(easset_only, "eva_grp1_sap", "sap")
easset_only = enrich_with_eva_details(easset_only, "eva_grp1_easset", "easset")

diff_eva = enrich_with_eva_details(diff_eva, "eva_grp1_sap", "sap")
diff_eva = enrich_with_eva_details(diff_eva, "eva_grp1_easset", "easset")

sap_only = add_kategori_aset(sap_only)
easset_only = add_kategori_aset(easset_only)
diff_eva = add_kategori_aset(diff_eva)

sap_only = add_ptj_slicer_col(sap_only)
easset_only = add_ptj_slicer_col(easset_only)
diff_eva = add_ptj_slicer_col(diff_eva)

def map_eva(df, col):
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().map(eva_desc_map)
    return df

sap_only = map_eva(sap_only, "eva_grp1_sap")
sap_only = map_eva(sap_only, "eva_grp1_easset")

easset_only = map_eva(easset_only, "eva_grp1_sap")
easset_only = map_eva(easset_only, "eva_grp1_easset")

diff_eva = map_eva(diff_eva, "eva_grp1_sap")
diff_eva = map_eva(diff_eva, "eva_grp1_easset")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.title("Tapisan")

kategori_filter = st.sidebar.radio("Kategori Aset", ["Semua", "Aset Alih", "Aset Tak Ketara"])

all_ptj = pd.concat(
    [
        sap_only.get("ptj_slicer_col", pd.Series(dtype=object)),
        easset_only.get("ptj_slicer_col", pd.Series(dtype=object)),
        diff_eva.get("ptj_slicer_col", pd.Series(dtype=object)),
        misclassified_low_value.get("ptj_slicer_col", pd.Series(dtype=object)),
    ],
    ignore_index=True,
)
ptj_list = sorted(all_ptj.dropna().unique().tolist())
ptj_list.insert(0, "Semua")
ptj_filter = st.sidebar.selectbox("PTJ", ptj_list)

st.sidebar.markdown(f"""
    <div style="
        margin-top:30px;
        padding:12px 15px;
        border:2px solid rgba(255,255,255,0.4);
        border-radius:8px;
        color:white;
        font-size:14px;
    ">
        <b>Tarikh Kemaskini:</b><br>
        {last_update_date}
    </div>
""", unsafe_allow_html=True)

# =========================
# FILTER HELPERS
# =========================
def filter_by_kategori(df):
    if "kategori_aset" not in df.columns:
        return df
    if kategori_filter == "Semua":
        return df
    return df[df["kategori_aset"] == kategori_filter]

def filter_by_ptj(df):
    if "ptj_slicer_col" not in df.columns:
        return df
    if ptj_filter == "Semua":
        return df
    return df[df["ptj_slicer_col"] == ptj_filter]

def clean_view(df):
    df = df.copy()
    cols_to_hide = ["_merge", "kategori_aset", "ptj_slicer_col", "prefix"]
    cols_to_hide += [c for c in df.columns if "eva_detail2" in c or "eva_detail3" in c]
    return df.drop(columns=[c for c in cols_to_hide if c in df.columns])

# APPLY FILTERS
sap_f = filter_by_ptj(filter_by_kategori(sap_only))
easset_f = filter_by_ptj(filter_by_kategori(easset_only))
diff_eva_f = filter_by_ptj(filter_by_kategori(diff_eva))
mis_f = filter_by_ptj(filter_by_kategori(misclassified_low_value))

# =========================
# CHART DATA
# =========================
def build_chart_data(df, issue_name):
    if df.empty:
        return pd.DataFrame(columns=["PTJ", "Jumlah Aset", "Isu"])

    ptj_series = None
    for col in ["sap_eva_detail2", "easset_eva_detail2", "eva_detail2"]:
        if col in df.columns:
            s = df[col].dropna()
            if not s.empty:
                ptj_series = s
                break

    if ptj_series is None:
        return pd.DataFrame(columns=["PTJ", "Jumlah Aset", "Isu"])

    g = ptj_series.groupby(ptj_series).size().reset_index(name="Jumlah Aset")
    g = g.rename(columns={ptj_series.name: "PTJ"})
    g = g.sort_values("Jumlah Aset", ascending=False)
    g["Isu"] = issue_name
    return g

chart1_df = build_chart_data(sap_f, "SAP sahaja")
chart2_df = build_chart_data(easset_f, "Easset sahaja")
chart3_df = build_chart_data(diff_eva_f, "Lokasi berbeza")
chart4_df = build_chart_data(mis_f, "Kelas 40000/41000 < RM2000")

def make_bar_chart(df, title):
    if df.empty:
        return None

    fig = px.bar(df, x="PTJ", y="Jumlah Aset", text="Jumlah Aset")

    max_y = df["Jumlah Aset"].max()
    headroom = max(2, int(max_y * 0.15))   # 15% ruang atas (min 2)

    fig.update_traces(
        marker_color="rgba(150,80,255,0.15)",
        marker_line_color="rgba(150,80,255,1)",
        marker_line_width=0.6,
        textposition="outside",
        cliponaxis=False,                 # ✅ penting: jangan potong text
        textfont=dict(size=12)
    )

    fig.update_layout(
        height=320,
        bargap=0.3,
        title=dict(text=title, x=0, xanchor="left",
                   font=dict(size=14, color="#778899", family="Arial")),
        showlegend=False,
        xaxis_title=None,
        yaxis_title=None,

        # ✅ bagi ruang untuk nombor atas bar
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0, max_y + headroom]
        ),

        xaxis=dict(showgrid=False, tickfont=dict(size=12)),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",

        # ✅ tambah top margin supaya text tak terpotong
        margin=dict(l=10, r=10, t=70, b=40),
    )

    return fig


def render_chart_card(df_chart, title):
    fig = make_bar_chart(df_chart, title)
    if fig is None:
        st.write("Tiada data untuk paparan.")
        return

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# MAIN
# =========================
st.title("Dashboard SAP Vs Easset")

# KPI
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
with kpi_col1:
    kpi_card("Jumlah Aset di SAP tetapi tiada di Easset", len(sap_f))
with kpi_col2:
    kpi_card("Jumlah Aset di Easset tetapi tiada di SAP", len(easset_f))
with kpi_col3:
    kpi_card("Jumlah Aset berlainan lokasi", len(diff_eva_f))
with kpi_col4:
    kpi_card("Aset Salah Klasifikasi", len(mis_f))

st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)


# CHARTS (2 x 2) — normal streamlit, tiada kotak custom
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    render_chart_card(chart1_df, "Isu 1 Aset ada di SAP tiada di Easset")

with row1_col2:
    render_chart_card(chart2_df, "Isu 2 Aset ada di Easset tiada di SAP")

with row2_col1:
    render_chart_card(chart3_df, "Isu 3 Lokasi berlainan SAP vs Easset")

with row2_col2:
    render_chart_card(chart4_df, "Isu 4 Aset salah klasifikasi Harta Modal")



# ================================
# TABLE 1
# ================================

view1 = clean_view(sap_f)

if not view1.empty:
    view1 = view1[["asset_no", "sub_no", "description_sap"]].rename(columns={
        "asset_no": "Asset No",
        "sub_no": "Sub No",
        "description_sap": "Keterangan"
    })
else:
    # pastikan view1 tetap ada column supaya tak error bila to_html/to_csv
    view1 = pd.DataFrame(columns=["Asset No", "Sub No", "Keterangan"])

view1 = view1.reset_index(drop=True)
view1.insert(0, "Bil", range(1, len(view1) + 1))

# --- tajuk + download sebaris ---
title_col, btn_col = st.columns([8, 2], vertical_alignment="center")

with title_col:
    st.markdown(
        "<h2 style='font-size:24px; font-weight:700; color:#8c92ac;'>"
        "Aset wujud dalam SAP Tiada di Easset"
        "</h2>",
        unsafe_allow_html=True
    )

with btn_col:
    csv_view1 = view1.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv_view1,
        file_name="aset_sap_tiada_easset.csv",
        mime="text/csv",
        use_container_width=True
    )

# --- table HTML (kekal macam kau buat) ---
table_html = view1.to_html(index=False)

st.markdown(
    f"""
    <div style="
        max-height: 260px;
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



# ================================
# TABLE 2
# ================================
view2 = clean_view(easset_f)

if not view2.empty:
    view2 = view2[["asset_no", "sub_no", "description_easset"]].rename(columns={
        "asset_no": "Asset No",
        "sub_no": "Sub No",
        "description_easset": "Keterangan"
    })
else:
    view2 = pd.DataFrame(columns=["Asset No", "Sub No", "Keterangan"])

view2 = view2.reset_index(drop=True)
view2.insert(0, "Bil", range(1, len(view2) + 1))

t2_title_col, t2_btn_col = st.columns([8, 2], vertical_alignment="center")

with t2_title_col:
    st.markdown(
        "<h2 style='font-size:24px; font-weight:700; color:#8c92ac;'>"
        "Aset wujud dalam Easset Tiada di SAP"
        "</h2>",
        unsafe_allow_html=True
    )

with t2_btn_col:
    csv_view2 = view2.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv_view2,
        file_name="aset_easset_tiada_sap.csv",
        mime="text/csv",
        use_container_width=True
    )

table_html2 = view2.to_html(index=False)

st.markdown(
    f"""
    <div style="
        max-height: 260px;
        overflow-y: auto;
        border-radius: 10px;
        border: 1px solid #F0E6FF;
        box-shadow: 0 4px 10px rgba(150, 80, 255, 0.07);
        margin-top: 8px;
    ">
        {table_html2}
    </div>
    """,
    unsafe_allow_html=True
)


# ================================
# TABLE 3
# ================================
view3 = clean_view(diff_eva_f)

if not view3.empty:
    view3 = view3[["asset_no", "sub_no", "description_sap", "sap_eva_desc", "easset_eva_desc"]].rename(columns={
        "asset_no": "Asset No",
        "sub_no": "Sub No",
        "description_sap": "Keterangan",
        "sap_eva_desc": "Lokasi SAP",
        "easset_eva_desc": "Lokasi Easset"
    })
else:
    view3 = pd.DataFrame(columns=["Asset No", "Sub No", "Keterangan", "Lokasi SAP", "Lokasi Easset"])

view3 = view3.reset_index(drop=True)
view3.insert(0, "Bil", range(1, len(view3) + 1))

t3_title_col, t3_btn_col = st.columns([8, 2], vertical_alignment="center")

with t3_title_col:
    st.markdown(
        "<h2 style='font-size:24px; font-weight:700; color:#8c92ac;'>"
        "Aset berlainan lokasi SAP vs Easset"
        "</h2>",
        unsafe_allow_html=True
    )

with t3_btn_col:
    csv_view3 = view3.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv_view3,
        file_name="aset_lokasi_berlainan.csv",
        mime="text/csv",
        use_container_width=True
    )

table_html3 = view3.to_html(index=False)

st.markdown(
    f"""
    <div style="
        max-height: 260px;
        overflow-y: auto;
        border-radius: 10px;
        border: 1px solid #F0E6FF;
        box-shadow: 0 4px 10px rgba(150, 80, 255, 0.07);
        margin-top: 8px;
    ">
        {table_html3}
    </div>
    """,
    unsafe_allow_html=True
)


# ================================
# TABLE 4
# ================================
view4 = clean_view(mis_f)

if not view4.empty:
    view4 = view4[["asset_no", "sub_no", "description", "acquisition_value"]].rename(columns={
        "asset_no": "Asset No",
        "sub_no": "Sub No",
        "description": "Keterangan",
        "acquisition_value": "Harga"
    })
else:
    view4 = pd.DataFrame(columns=["Asset No", "Sub No", "Keterangan", "Harga"])

view4 = view4.reset_index(drop=True)
view4.insert(0, "Bil", range(1, len(view4) + 1))

t4_title_col, t4_btn_col = st.columns([8, 2], vertical_alignment="center")

with t4_title_col:
    st.markdown(
        "<h2 style='font-size:24px; font-weight:700; color:#8c92ac;'>"
        "Aset salah klasifikasi harta modal"
        "</h2>",
        unsafe_allow_html=True
    )

with t4_btn_col:
    csv_view4 = view4.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv_view4,
        file_name="aset_salah_klasifikasi.csv",
        mime="text/csv",
        use_container_width=True
    )

table_html4 = view4.to_html(index=False)

st.markdown(
    f"""
    <div style="
        max-height: 260px;
        overflow-y: auto;
        border-radius: 10px;
        border: 1px solid #F0E6FF;
        box-shadow: 0 4px 10px rgba(150, 80, 255, 0.07);
        margin-top: 8px;
    ">
        {table_html4}
    </div>
    """,
    unsafe_allow_html=True
)
