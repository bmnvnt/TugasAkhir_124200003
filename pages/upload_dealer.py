import streamlit as st
import pandas as pd

@st.cache_data
def load_dealer(uploaded_dealer):
    if uploaded_dealer:
        dealer = pd.read_csv(uploaded_dealer, sep=';')
        return dealer
    return None

# Menyimpan data ke session_state agar tidak hilang saat reload
if 'dealer1' not in st.session_state:
    st.session_state['dealer1'] = pd.read_csv('./data/data_dealer_penjualan.csv', sep=';')

if 'dealer2' not in st.session_state:
    st.session_state['dealer2'] = pd.read_csv('./data/data_dealer_purna.csv', sep=';')

st.title(""" Aplikasi Klastering Market Coverage Area Wuling \n """)
# st.markdown("Aplikasi ini dibuat untuk membantu PT. SGMW Motor Indonesia dalam mengolah data Sales dan After Sales.")

uploaded_dealer1 = st.file_uploader("Pilih file data lokasi dealer penjualan", type=["csv"])
uploaded_dealer2 = st.file_uploader("Pilih file data lokasi dealer servis", type=["csv"])

# Menangani file pertama
if uploaded_dealer1 is not None:
    st.session_state['dealer1'] = load_dealer(uploaded_dealer1)
    st.success("Upload data lokasi dealer penjualan berhasil")
    with st.expander('Lihat data lokasi dealer penjualan.'):
        st.write("Data lokasi berhasil diunggah.", st.session_state['dealer1'])    
else:
    if st.session_state['dealer1'] is not None:
        with st.expander('Lihat data lokasi dealer penjualan.'):
            st.write("Data lokasi berhasil diunggah.", st.session_state['dealer1'])
        # st.success("Data Penjualan berhasil diunggah.")
        # st.dataframe(st.session_state['dealer1'])
    else:
        st.error("Belum ada data lokasi dealer penjualan yang diunggah.")

# Menangani dealer kedua
if uploaded_dealer2 is not None:
    st.session_state['dealer2'] = load_dealer(uploaded_dealer2)
    st.success("Upload data lokasi dealer servis berhasil")
    with st.expander('Lihat data lokasi dealer servis.'):
        st.write("Data lokasi berhasil diunggah.", st.session_state['dealer2'])
else:
    if st.session_state['dealer2'] is not None:
        with st.expander('Lihat data lokasi dealer servis.'):
            st.write("Data lokasi berhasil diunggah.", st.session_state['dealer2'])
        # st.success("Data Purna Jual berhasil diunggah.")    
        # st.dataframe(st.session_state['dealer2'])
    else:
        st.error("Belum ada data lokasi dealer servis yang diunggah.")



