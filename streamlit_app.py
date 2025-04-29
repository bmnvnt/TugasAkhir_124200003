import streamlit as st

st.set_page_config(
    page_title="Wuling Klastering",
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
    title="Pemodelan Data",
    icon=":material/settings:",
)
visual_data = st.Page(
    "pages/visual_data.py",
    title="Visualisasi Data",
    icon=":material/map:",
)

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "File": [upload_data],
        "Proses": [process_data, uji_data, visual_data],
    }
)

expander = st.sidebar.expander("What is this?")
expander.write(
    """Aplikasi ini dibuat untuk membantu PT. SGMW Motor Indonesia dalam mengolah data Sales dan After Sales."""
)

# --- RUN NAVIGATION ---
pg.run()