import streamlit as st
import pandas as pd

@st.cache_data
def load_dataset(uploaded_file):
    if uploaded_file:
        dataset = pd.read_csv(uploaded_file, sep=';')
        return dataset
    return None

if 'dataset1' not in st.session_state:
    st.session_state['dataset1'] = None

if 'dataset2' not in st.session_state:
    st.session_state['dataset2'] = None

st.title(""" Aplikasi Clustering Market Coverage Area Wuling \n """)

uploaded_file1 = st.file_uploader("Pilih file data penjualan", type=["csv"])
uploaded_file2 = st.file_uploader("Pilih file data servis", type=["csv"])
st.session_state['dealer1'] = pd.read_csv('./data/data_dealer_penjualan.csv', sep=';')    #data dealer penjualan
st.session_state['dealer2'] = pd.read_csv('./data/data_dealer_purna.csv', sep=';')      #data dealer servis

if uploaded_file1 is not None:
    st.session_state['dataset1'] = load_dataset(uploaded_file1)
    st.success("Upload data penjualan berhasil")
else:
    if st.session_state['dataset1'] is not None:
        st.success("Data Penjualan berhasil diunggah.")
    else:
        st.error("Belum ada data penjualan yang diunggah.")

if uploaded_file2 is not None:
    st.session_state['dataset2'] = load_dataset(uploaded_file2)
    st.success("Upload data servis berhasil")
else:
    if st.session_state['dataset2'] is not None:
        st.success("Data servis berhasil diunggah.")
    else:
        st.error("Belum ada data servis yang diunggah.")


