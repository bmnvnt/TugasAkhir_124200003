import streamlit as st

st.set_page_config(
    page_title="Wuling Clustering",
    page_icon="./img/logored.png",
    layout="wide"
)

st.logo(image="./img/logo.png",
        size="large",
        icon_image="./img/wulingred.png")

# --- PAGE SETUP ---
upload_data = st.Page(
    "pages/upload_data.py",
    title="Upload Data",
    icon=":material/upload:",
    default=True,
)
# upload_dealer = st.Page(
#     "pages/upload_dealer.py",
#     title="Upload Data Lokasi",
#     icon=":material/home:",
# )
process_data = st.Page(
    "pages/process_data.py",
    title="Pengolahan Data",
    icon=":material/sync:",
)
uji_data = st.Page(
    "pages/uji_data.py",
    title="Evaluasi Data",
    icon=":material/settings:",
)
visual_data = st.Page(
    "pages/visual_data.py",
    title="Visualisasi Data",
    icon=":material/map:",
)

pg = st.navigation(
    {
        "File": [upload_data],
        "Proses": [process_data, uji_data, visual_data],
    }
)

expander = st.sidebar.expander("Aplikasi apa ini?")
expander.write(
    """Aplikasi ini dibuat untuk membantu PT. SGMW Motor Indonesia dalam mengolah data Sales dan After Sales
       dengan menggunakan machine learning untuk mengklasterisasi wilayah sekaligus menampilkannya ke dalam peta.
       Serta menganalisa data penjualan dan purna jual yang hasilnya disajikan ke dalam grafik-grafik analisis."""
)

# --- RUN NAVIGATION ---
pg.run()