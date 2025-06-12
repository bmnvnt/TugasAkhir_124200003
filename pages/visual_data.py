import streamlit as st
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import folium
# from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


st.html('style.html')
st.title("Visualisasi Data")

tab1,tab2 = st.tabs(["Clustering","Analisa Data"])
if st.session_state.df_combined is not None:
    with tab1:
        if 'gdf' not in st.session_state:
            st.session_state.gdf = gpd.read_file('./data/newindo.json')

        gdf = st.session_state.gdf

        st.header("Peta Clustering Market Coverage Area Wuling di Indonesia")
        k_slider = st.slider('Pillih jumlah klaster', 2, 10, value=2)

        jumlah_data1 = len(st.session_state['df_penjualan1'])
        formatted_number1 = f"{jumlah_data1:,.0f}"

        jumlah_data2 = len(st.session_state['df_servis1'])
        formatted_number2 = f"{jumlah_data2:,.0f}"

        # K-means clustering
        kmeans = KMeans(n_clusters=k_slider, random_state=42)
        kmeans.fit(st.session_state.data_standardized)
            
        clusters = pd.DataFrame(kmeans.labels_, columns=['Cluster'])
            
        data_cleansed = st.session_state.df_combined.copy()
        data_cleansed['Cluster'] = clusters +1  

        finalpenjualan = pd.merge(st.session_state['df_penjualan1'], data_cleansed[['Provinces','Cluster']], left_on='Provinces', right_on='Provinces', how='right')
        finalservis = pd.merge(st.session_state['df_servis1'], data_cleansed[['Provinces','Cluster']], left_on='Provinces', right_on='Provinces', how='right')
        gdf = gdf.merge(data_cleansed[['Provinces', 'Total penjualan', 'Total servis','Total dealer', 'Cluster']], how='left', left_on='name', right_on='Provinces')

        left_map, right_summary = st.columns([2, 0.65])

        with left_map:
            # Membuat peta
            map_indonesia = folium.Map(location=[-3.0, 118.0], zoom_start=4.5)

            #layer tipe peta
            folium.TileLayer(
            tiles='CartoDB positron',
            attr='',
            ).add_to(map_indonesia)   

            cluster_colors = {1: 'Red',
                              2: 'Orange',
                              3: 'Yellow',
                              4: 'Green',  
                              5: 'Blue', 
                              6: 'Purple', 
                              7: 'Pink',  
                              8: 'Brown',  
                              9: 'Dark Brown', 
                              10:'Cream',  
            }

            st.session_state['cluster_colors'] = cluster_colors

            popup = folium.GeoJsonTooltip(
                    fields=["Provinces", "Total penjualan", "Total servis", "Total dealer", "Cluster"],
                    aliases=["Provinsi", "Total Penjualan", "Total Servis", "Total Dealer", "Cluster"],
                    localize=True,
                    labels=True,
                )
            
            #layer cluster
            folium.GeoJson(
                    gdf,
                    name="Cluster",
                    zoom_on_click=True,
                    highlight_function=lambda feature: {
                "fillColor": (
                    "yellow"
                ), 'fillOpacity' : 0.1
            },
                    style_function=lambda feature: {
                        'fillColor': cluster_colors.get(feature['properties']['Cluster'], 'gray'),
                        'color': 'black',
                        'weight': 1,
                        'fillOpacity': 0.8
                    },
                    tooltip=popup
                ).add_to(map_indonesia)
            
            #layer batas wilayah
            folium.GeoJson(gdf,show=False, name="Batas Wilayah", zoom_on_click=True,
                highlight_function=lambda feature: {
                "fillColor": (
                    "green" if "e" in feature["properties"]["name"].lower() else "#ffff00"
                ),
            }).add_to(map_indonesia)
                
            folium.LayerControl().add_to(map_indonesia)

            #peta ke file HTML
            map_indonesia.save('map_without_watermark.html') 

            #nampilin peta di Streamlit
            folium_static(map_indonesia, width=None, height=460)  # Ukuran peta

        with right_summary:
            st.subheader("Market Summary")
            st.html('<span class="high_indicator"></span>')
            prov = len(data_cleansed['Provinces'])
            totalprov = f"{prov:,.0f}"
            st.metric("Provinsi", totalprov)
            st.metric("Total Penjualan", formatted_number1)
            st.metric("Total Service", formatted_number2)
            st.metric("Target Penjualan Tahunan", formatted_number1 + "/24000")
        
        #expander
        with st.expander('Lihat Data JSON (GeoData)'):
            st.write("Data JSON yang dimuat:", gdf)
        
        #nampilin jumlah data per cluster
        cluster_counts = data_cleansed.groupby('Cluster').size()
        kiri, kanan = st.columns(2)
        with kiri:
            jumlah_cluster2 = go.Figure(data=[go.Pie(labels=cluster_counts.index, values=cluster_counts.values, hole=.3)])
            jumlah_cluster2.update_layout(title={'text':'Persentase Cluster', 'x':0.5, 'xanchor':'center', 'yanchor':'top'},
                                         uniformtext_minsize=16, uniformtext_mode='hide'
                                       )
            st.plotly_chart(jumlah_cluster2)
            
        with kanan:
            jumlah_cluster = px.bar(x=cluster_counts.index,
                                    y=cluster_counts.values,
                                    labels={'x': 'Cluster', 'y': 'Jumlah Anggota'}, title="Perbandingan Cluster", text_auto=True)
            jumlah_cluster.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False,)
            jumlah_cluster.update_layout(title={'x':0.5, 'xanchor':'center', 'yanchor':'top'},
                                xaxis={'categoryorder':'total descending'}, showlegend=False
                            )
            st.plotly_chart(jumlah_cluster)
        

        nama_tabs=[f"Cluster {i+1}" for i in range (k_slider)]
        tabs=st.tabs(nama_tabs)
        # Mengelompokkan data berdasarkan cluster dan mencari nilai maksimum dari penjualan setiap cluster
        max_penjualan = data_cleansed.groupby('Cluster')['Total penjualan'].max()

        # Mengurutkan berdasarkan nilai maksimum penjualan dari terbesar ke terkecil
        urutan_penjualan = max_penjualan.sort_values(ascending=True)
        # urutan_penjualan['Urutan'] = urutan_penjualan['Cluster'].apply(lambda x: urutan_daerah.index(x))
        # st.write(urutan_penjualan)

        for i in range(k_slider):
            
            with tabs[i]:
                rank = urutan_penjualan.index[i]
                cluster_penjualan = finalpenjualan[finalpenjualan['Cluster'] == rank]
                cluster_servis = finalservis[finalservis['Cluster'] == rank]
                cluster_data = data_cleansed[data_cleansed['Cluster'] == rank]
                st.write(f"### Cluster {i+1}:")
                st.subheader('Karakteristik Cluster')
                min_sales = cluster_data['Total penjualan'].min()
                max_sales = cluster_data['Total penjualan'].max()
                min_servis = cluster_data['Total servis'].min()
                max_servis = cluster_data['Total servis'].max()
                min_dealer = cluster_data['Total dealer'].min()
                max_dealer = cluster_data['Total dealer'].max()

                cl_number = i+1
                color = st.session_state['cluster_colors'].get(cl_number, "Color not found")

                min_sales = f"{min_sales:,.0f}"
                max_sales = f"{max_sales:,.0f}"
                min_servis = f"{min_servis:,.0f}"
                max_servis = f"{max_servis:,.0f}"
                min_dealer = f"{min_dealer:,.0f}"
                max_dealer = f"{max_dealer:,.0f}"
                
                st.write(f"Cluster {i+1} {color}: Cluster ini berisi provinsi dengan dealer dengan jumlah mulai dari {min_dealer} hingga {max_dealer}, penjualan mulai dari {min_sales} - {max_sales} mobil dan melayani {min_servis} - {max_servis} servis mobil selama 6 bulan")
                
                with st.expander('Lihat Data per cluster'):
                    st.write("", cluster_data)
                    
                kiri, kanan = st.columns(2)
                with kiri:
                    top5 = cluster_penjualan.groupby('Provinces')['Total penjualan'].sum().reset_index()
                    top5 = top5.sort_values(by='Total penjualan', ascending=False).head(10)

                    fig_cl_kiri = px.bar(top5, x="Provinces", y="Total penjualan", title="Top 10 Provinsi vs Penjualan", text_auto=True)
                    fig_cl_kiri.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False,)
                    fig_cl_kiri.update_layout(title={'x':0.5, 'xanchor':'center', 'yanchor':'top'},
                            xaxis={'categoryorder':'total descending'}, showlegend=False
                        )
                    st.plotly_chart(fig_cl_kiri)

                with kanan:
                    top5 = cluster_penjualan.groupby('Models')['Total penjualan'].sum().reset_index()
                    top5 = top5.sort_values(by='Total penjualan', ascending=False).head(5)
                    tes = finalpenjualan.groupby('Models')['Series'].unique().reset_index()
                    tes['Series'] = tes['Series'].astype('str')

                    top5 = top5.merge(tes[['Models','Series']], how='left', on='Models')
                    # st.write(top5)
                    fig_cl_kanan = px.bar(top5, x="Models", y="Total penjualan", title="Top 5 Model Terlaris", text_auto=True, color='Series')
                    fig_cl_kanan.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False,)
                    fig_cl_kanan.update_layout(title={'x':0.5, 'xanchor':'center', 'yanchor':'top'},
                            xaxis={'categoryorder':'total descending'}, showlegend=False
                        )
                    st.plotly_chart(fig_cl_kanan)

                kiri2, kanan2 = st.columns(2)
                with kiri2:
                    top5 = cluster_servis.groupby('Provinces')['Total servis'].sum().reset_index()
                    top5 = top5.sort_values(by='Total servis', ascending=False).head(10)

                    fig_cl_kiri = px.bar(top5, x="Provinces", y="Total servis", title="Top 10 Provinsi vs Servis", text_auto=True)
                    fig_cl_kiri.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False,)
                    fig_cl_kiri.update_layout(title={'x':0.5, 'xanchor':'center', 'yanchor':'top'},
                            xaxis={'categoryorder':'total descending'}, showlegend=False
                        )
                    st.plotly_chart(fig_cl_kiri)

                with kanan2:
                    top5 = cluster_servis.groupby('Models')['Total servis'].sum().reset_index()
                    top5 = top5.sort_values(by='Total servis', ascending=False).head(5)
                    tes = finalservis.groupby('Models')['Series'].unique().reset_index()
                    tes['Series'] = tes['Series'].astype('str')

                    top5 = top5.merge(tes[['Models','Series']], how='left', on='Models')
                    # st.write(top5)
                    fig_cl_kanan = px.bar(top5, x="Models", y="Total servis", title="Top 5 Model Servis",  text_auto=True, color='Series')
                    fig_cl_kanan.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False,)
                    fig_cl_kanan.update_layout(title={'x':0.5, 'xanchor':'center', 'yanchor':'top'},
                            xaxis={'categoryorder':'total descending'}, showlegend=False
                        )
                    st.plotly_chart(fig_cl_kanan)
            
        # Visualisasi hasil clustering (scatter plot)
        with st.expander('Grafik Scatter Plot Klaster'):
            st.subheader('Visualisasi Hasil Clustering')
            fig, ax = plt.subplots(figsize=(14, 6))
            sns.scatterplot(x=data_cleansed.iloc[:, 1], y=data_cleansed.iloc[:, 2], hue=data_cleansed['Cluster'], palette=cluster_colors, ax=ax)
            ax.set_title('Visualisasi Hasil Clustering')
            st.pyplot(fig)

    with tab2:

        total1,total2,total3=st.columns(3,gap='small')
        with total1:
            st.info('Sales Activity',icon="💲")
            st.metric(label="Total Penjualan",value=formatted_number1)

        with total2:
            st.info('Service Activity',icon="🔧")
            st.metric(label="Total Servis",value=formatted_number2)

        with total3:
            st.info('Wilayah',icon="🏠")
            st.metric(label="Total Provinsi",value=totalprov)


        penjualan, servis = st.tabs(["Data Penjualan", "Data Servis"])

        with penjualan:
            #filter
            prov_filter = st.multiselect("Pilih provinsi", options=finalpenjualan['Provinces'].unique(), default=None, key="prv")
            series_filter = st.multiselect("Pilih series", options=finalpenjualan['Series'].unique(), default=None, key = "srs")

            l,r = st.columns([2.02, 1])
            
            with l:
                if series_filter and prov_filter:
                    filtered_df = finalpenjualan[
                        (finalpenjualan['Series'].isin(series_filter)) &
                        (finalpenjualan['Provinces'].isin(prov_filter))
                    ]
                elif series_filter:
                    filtered_df = finalpenjualan[finalpenjualan['Series'].isin(series_filter)]
                elif prov_filter:
                    filtered_df = finalpenjualan[finalpenjualan['Provinces'].isin(prov_filter)]
                    
                else:
                    filtered_df = finalpenjualan

                # st.write(filtered_df)
                total = filtered_df.groupby('Report date')['Total penjualan'].sum().reset_index()
                # st.write(total)
                if len(prov_filter) == 0:
                    title="Total Penjualan Bulanan di Indonesia"
                else:
                    title=f'Total Penjualan Bulanan di {", ".join(map(str, prov_filter))}'

                fig_sales=px.line(
                            total,
                            x="Report date",
                            y="Total penjualan",
                            markers=True,
                            # color = "Cluster"
                            title=title,
                            height=398
                        )
                fig_sales.update_layout(title={'x':0.5, 'xanchor':'center', 'yanchor':'top'})
                st.plotly_chart(fig_sales)

            with r:
                # st.write(filtered_df)
                total_dl = filtered_df["Dealer name"].nunique()
                st.metric("Total Dealer", total_dl)

                total_sl = filtered_df["Total penjualan"].sum()
                total_sl = f"{total_sl:,.0f}"
                st.metric("Total Penjualan", total_sl)

                total_slc = filtered_df["sales consultant"].nunique()
                st.metric("Total Sales Consultant", total_slc)
                
                total_mdl = filtered_df["Models"].nunique()
                st.metric("Total Models", total_mdl)
            
            kiri, tengah, kanan = st.columns(3)
            with kiri:
                total3 = filtered_df.groupby('Customer type')['Total penjualan'].sum().reset_index()
                labels = total3['Customer type']
                values = total3['Total penjualan']
                
                fig_sales3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
                fig_sales3.update_layout(title={'text':'Persentase Tipe Pelanggan', 'x':0.5, 'xanchor':'center', 'yanchor':'top'},
                                         uniformtext_minsize=16, uniformtext_mode='hide'
                                       )
                st.plotly_chart(fig_sales3)

            with tengah:
                top5 = filtered_df.groupby('sales consultant')['Total penjualan'].sum().reset_index()
                top5 = top5.sort_values(by='Total penjualan', ascending=False).head(5)

                fig2 = px.bar(top5, x="sales consultant", y="Total penjualan", title="Posisi 5 Teratas Sales Consultant", text_auto=True)
                fig2.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False,)
                fig2.update_layout(title={'x':0.5, 'xanchor':'center', 'yanchor':'top'},
                        xaxis={'categoryorder':'total descending'}
                    )
                st.plotly_chart(fig2)

            with kanan:
                total4 = filtered_df.groupby('Promotion')['Total penjualan'].sum().reset_index()
                labels = total4['Promotion']
                values = total4['Total penjualan']
                
                # Use `hole` to create a donut-like pie chart
                fig_sales4 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, 
                                                    textfont_size=16, 
                                                    )])
                fig_sales4.update_layout(title={'text':'Persentase Promotion yang digunakan', 'x':0.5, 'xanchor':'center', 'yanchor':'top'},
                                         uniformtext_minsize=12, uniformtext_mode='hide'
                                       )
                st.plotly_chart(fig_sales4)

            kiri_bawah, tengah_bawah, kanan_bawah = st.columns(3)

            with kiri_bawah:
                total2 = filtered_df.groupby('Models')['Total penjualan'].sum().reset_index()
                labels = total2['Models']
                values = total2['Total penjualan']
                
                # Use `hole` to create a donut-like pie chart
                fig_sales2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
                fig_sales2.update_layout(title={'text':'Persentase Model yang terjual', 'x':0.5, 'xanchor':'center', 'yanchor':'top'}
                                       )
                st.plotly_chart(fig_sales2)

            with tengah_bawah:
                top5 = filtered_df.groupby('Colour')['Total penjualan'].sum().reset_index()
                top5 = top5.sort_values(by='Total penjualan', ascending=False).head(5)

                fig2 = px.bar(top5, x="Colour", y="Total penjualan", title="Posisi 5 Warna Mobil", text_auto=True)
                fig2.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False,)
                fig2.update_layout(title={'x':0.5, 'xanchor':'center', 'yanchor':'top'},
                        xaxis={'categoryorder':'total descending'}
                    )
                st.plotly_chart(fig2)

            with kanan_bawah:
                total4 = filtered_df.groupby('Payment method')['Total penjualan'].sum().reset_index()
                labels = total4['Payment method']
                values = total4['Total penjualan']
                
                fig_sales4 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, 
                                                    textfont_size=16, 
                                                    # marker=dict(pattern=dict(shape=["x", "+", "-"]))
                                                    )])
                fig_sales4.update_layout(title={'text':'Persentase Metode Pembayaran yang digunakan', 'x':0.5, 'xanchor':'center', 'yanchor':'top'},
                                         uniformtext_minsize=12, uniformtext_mode='hide'
                                       )
                st.plotly_chart(fig_sales4)


        with servis:
            prov_filter2 = st.multiselect("Pilih provinsi", options=finalservis['Provinces'].unique(), default=None, key="prov")
            series_filter2 = st.multiselect("Pilih series", options=finalservis['Series'].unique(), default=None, key="series")

            

            l,r = st.columns([2.02, 1])

            with l:
                if series_filter2 and prov_filter2:
                    filtered_df = finalservis[
                        (finalservis['Series'].isin(series_filter2)) &
                        (finalservis['Provinces'].isin(prov_filter2))
                    ]
                elif series_filter2:
                        filtered_df = finalservis[finalservis['Series'].isin(series_filter2)]
                elif prov_filter2:
                        filtered_df = finalservis[finalservis['Provinces'].isin(prov_filter2)]
                else:
                        filtered_df = finalservis

                total3 = filtered_df.groupby('Order time')['Total servis'].sum().reset_index()

                if len(prov_filter2) == 0:
                    title2="Total Servis Bulanan di Indonesia"
                else:
                    title2=f'Total Servis Bulanan di {", ".join(map(str, prov_filter2))}'

                fig_servis3=px.line(
                            total3,
                            x="Order time",
                            y="Total servis",
                            markers=True,
                            # color = "Cluster"
                            title=title2,
                            height=398
                        )
                fig_servis3.update_layout(title={'x':0.5, 'xanchor':'center', 'yanchor':'top'})
                st.plotly_chart(fig_servis3)

            with r:
                # st.write(filtered_df)
                total_dl = filtered_df["Dealer name"].nunique()
                st.metric("Total Dealer", total_dl)

                total_sr = filtered_df["Total servis"].sum()
                total_sr = f"{total_sr:,.0f}"
                st.metric("Total servis", total_sr)

                total_src = filtered_df["Service advisor"].nunique()
                st.metric("Total Service Advisor", total_src)
                
                total_mdl = filtered_df["Models"].nunique()
                st.metric("Total Models", total_mdl)

            kiri, tengah, kanan = st.columns(3)
            with kiri:
                total4 = filtered_df.groupby('Series')['Total servis'].sum().reset_index()
                labels4 = total4['Series']
                values4 = total4['Total servis']
                
                # Use `hole` to create a donut-like pie chart
                fig_servis2 = go.Figure(data=[go.Pie(labels=labels4, values=values4, hole=.3)])
                fig_servis2.update_layout(title={'text':'Persentase Series vs Servis','x':0.5, 'xanchor':'center', 'yanchor':'top'}
                                       )
                st.plotly_chart(fig_servis2)

            with tengah:
                top5 = filtered_df.groupby('Provinces')['Total servis'].sum().reset_index()
                top5 = top5.sort_values(by='Total servis', ascending=False).head(10)

                fig2 = px.bar(top5, x="Provinces", y="Total servis", title="Top 10 Provinsi vs Servis", text_auto=True)
                fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
                fig2.update_layout(
                        xaxis={'categoryorder':'total descending'}, title={'x':0.5, 'xanchor':'center', 'yanchor':'top'}
                    )
                st.plotly_chart(fig2)

            with kanan:
                total2 = filtered_df.groupby('Models')['Total servis'].sum().reset_index()
                labels = total2['Models']
                values = total2['Total servis']
                
                # Use `hole` to create a donut-like pie chart
                fig_sales2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
                fig_sales2.update_layout(title={'text':'Persentase Model yang servis'}
                                       )
                st.plotly_chart(fig_sales2)

else:
    st.error("Pemodelan data belum dilakukan. Harap lakukan pemodelan data terlebih dahulu.")