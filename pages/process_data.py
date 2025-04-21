import streamlit as st
import pandas as pd

st.title("Pengolahan Data")

pro1,pro2,pro3,pro4 = st.tabs(["Raw Data","Cleansing Data", "Merging Data", "Result"])
st.session_state.df_combined = None

#RAW DATA
with pro1:
    if st.session_state['dataset1'] is not None:
        st.subheader("Raw Data")
        jumlah_data1 = len(st.session_state['dataset1'])
        formatted_number1 = f"{jumlah_data1:,.0f}"
        st.write(f"Digunakan dataset penjualan dari PT. SGMW Motor Indonesia dengan {formatted_number1} jumlah data.")
        st.dataframe(st.session_state['dataset1'])
        # st.dataframe(st.session_state['dealer1'])
    else:
        st.error("Data penjualan belum diunggah. Harap unggah file terlebih dahulu.")

    if st.session_state['dataset2'] is not None:
        jumlah_data2 = len(st.session_state['dataset2'])
        formatted_number2 = f"{jumlah_data2:,.0f}"
        st.write(f"Digunakan dataset purna jual dari PT. SGMW Motor Indonesia dengan {formatted_number2} jumlah data.")
        st.dataframe(st.session_state['dataset2'])
        # st.dataframe(st.session_state['dealer2'])
    else:
        st.error("Data purna jual belum diunggah. Harap unggah file terlebih dahulu.")
 
 
#CLEANSING DATA
with pro2:
    if st.session_state['dataset1'] is not None:
        st.subheader("Cleansing Data")
        st.markdown("Dihapus kolom-kolom yang kosong dari data penjualan:")
        df1 = st.session_state['dataset1']

        df1 = df1.drop(['Provinces', 'Order number', 'Plate registration dealer code', 'Plate registration dealer name', 'Plate No.',
                        'Certification No', 'Sales Area', 'Wuling Sales ID', 'customer source', 'City & Province',
                        'SubDistrict', 'District/Cities', 'City', 'Material code', 'VIN', 'Charging pile program',
                        'Configuration', 'Order Status', 'Customer level', 'Customer No', 'Street',
                        'Contact number', 'Vehicle delivery date', 'Coupon code', 'Leasing'], axis=1)
        df1['Colour'] = df1['Colour'].replace('Candy white', 'Candy White')
        df1['Total penjualan']=1
        st.session_state['df1'] = df1
        st.dataframe(df1)
    else:
        st.error("Data penjualan belum diunggah. Harap unggah file terlebih dahulu.")

    if st.session_state['dataset2'] is not None:
        st.markdown("Dihapus kolom-kolom yang kosong dari data purna jual:")
        df2 = st.session_state['dataset2']

        df2 = df2.drop(['Order No.', 'Settlement time','Plate No.','Order type','VIN','Order status','Customer Name',
                    'customer address','Contact name','Contact mobile phone'], axis=1)

        df2['Total servis']=1
        # Ubah ke datetime format dari dd/mm/yyyy
        df2['Order time'] = pd.to_datetime(df2['Order time'])

        # Format ulang jadi yyyy-mm-dd (kalau ingin string)
        df2['Order time'] = df2['Order time'].dt.strftime('%Y-%m-%d')
        st.session_state['df2'] = df2
        st.dataframe(df2)
    else:
        st.error("Data purna jual belum diunggah. Harap unggah file terlebih dahulu.")


#MERGING DATA
with pro3:
    if st.session_state['dataset1'] is not None:
        st.subheader("Merging Data")
        st.markdown("Dilakukan agregasi data penjualan berdasarkan provinsi:")
        dl1 = st.session_state['dealer1']
        filter1 = df1[~df1['Dealer name'].isin(dl1['Dealer name'])]
        df_penjualan1 = pd.merge(df1, dl1, on='Dealer name')
        jumlah_filter1 = len(filter1)
        jumlah_filter1 = f"{jumlah_filter1:,.0f}"
        st.session_state['df_penjualan1'] = df_penjualan1
        st.dataframe(df_penjualan1)
        with st.expander(f'Lihat {jumlah_filter1} data dealer penjualan yang tidak memiliki lokasi.'):
            st.write(f"Data dari dealer yang memiliki lokasi ada {jumlah_filter1}.", filter1)
    else:
        st.error("Data penjualan belum diunggah. Harap unggah file terlebih dahulu.")

    if st.session_state['dataset2'] is not None:
        st.markdown("Dilakukan agregasi data servis berdasarkan provinsi:")
        dl2 = st.session_state['dealer2']
        filter2 = df2[~df2['Dealer name'].isin(dl2['Dealer name'])] 
        df_servis1 = pd.merge(df2, dl2, on='Dealer name')
        jumlah_filter2 = len(filter2)
        jumlah_filter2 = f"{jumlah_filter2:,.0f}"
        st.session_state['df_servis1'] = df_servis1
        st.dataframe(df_servis1)
        with st.expander(f'Lihat {jumlah_filter2} data dealer servis yang tidak memiliki lokasi.'):
            st.write("", filter2)
    else:
        st.error("Data purna jual belum diunggah. Harap unggah file terlebih dahulu.")

#GROUPBY
with pro4:
    if st.session_state['dataset1'] is not None:
        st.subheader("Summary Data")
        st.markdown("Dilakukan penggabungan data penjualan dengan data lokasi dealer:")
        group1 = df_penjualan1.groupby(df_penjualan1['Provinces'])['Total penjualan'].sum().reset_index()

        st.dataframe(group1)
    else:
        st.error("Data penjualan belum diunggah. Harap unggah file terlebih dahulu.")

    if st.session_state['dataset2'] is not None:
        st.markdown("Dilakukan penggabungan data penjualan dengan data lokasi dealer:")
        group2 = df_servis1.groupby(df_servis1['Provinces'])['Total servis'].sum().reset_index()

        st.dataframe(group2)


        st.subheader("Result")
        # st.markdown("Dilakukan penggabungan data penjualan dengan data lokasi dealer:")
        df_combined = pd.merge(group1, group2, on='Provinces', how='outer')
        df_combined = df_combined.fillna(0)
        st.session_state.df_combined = df_combined
        st.dataframe(df_combined)
    else:
        st.error("Data purna jual belum diunggah. Harap unggah file terlebih dahulu.")
