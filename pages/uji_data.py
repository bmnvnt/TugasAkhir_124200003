import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Pemodelan Data")
tab1, tab2, tab3 = st.tabs(["Standarization", "Elbow Method", "Silhoutte Score"])
if st.session_state.df_combined is not None:
    with tab1:
        scaler = StandardScaler()
        data_standardized = pd.DataFrame(scaler.fit_transform(st.session_state.df_combined.select_dtypes(include=[np.number])))

        st.session_state.data_standardized = data_standardized
                
        st.subheader('Data Standarisasi')
        st.dataframe(data_standardized)
                
        st.subheader('Scatter Plot Sebelum dan Sesudah Standarisasi')
                
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
                
        sns.scatterplot(x=st.session_state.df_combined.iloc[:, 0], y=st.session_state.df_combined.iloc[:, 1], ax=axes[0])
        axes[0].set_title('Sebelum Standarisasi')
                
        sns.scatterplot(x=data_standardized.iloc[:, 0], y=data_standardized.iloc[:, 1], ax=axes[1])
        axes[1].set_title('Setelah Standarisasi')
                
        st.pyplot(fig)

        data_standardized = st.session_state.data_standardized
        
        # Menentukan nilai k terbaik dengan silhouette score
    k_range = range(2, 11)
    silhouette_scores = []
        
    with tab2:
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(data_standardized)
            silhouette_scores.append(silhouette_score(data_standardized, kmeans.labels_))
            
            # Tabel hasil silhouette score untuk k=2 sampai k=10
        k_scores_df = pd.DataFrame({
            'K': k_range,
            'Silhouette Score': silhouette_scores
        })
        st.subheader('Silhouette Score untuk Nilai K (2-10)')
        st.dataframe(k_scores_df)

        # Pilih K terbaik
        optimal_k = k_range[np.argmax(silhouette_scores)]
        st.write(f'Nilai K terbaik berdasarkan Silhouette Score adalah K = {optimal_k}')
        
    with tab3:
        wcss = []
        for  k  in np.arange(1, 10+1):
            kmeans = KMeans(n_clusters = k , random_state=5)
            kmeans.fit(data_standardized)
            wcss.append( kmeans.inertia_ )   
                            
                # 6. elobw method 를 이용해서, 차트로 보여준다.
        fig1 = plt.figure(figsize=(14,6))
        x = np.arange(1, 10+1)
        plt.plot(x, wcss)
        plt.title('Elbow method')
        plt.xlabel('Number of clusters')
        plt.ylabel('wcss')
        st.pyplot(fig1)

        # Pilih K terbaik
        optimal_k = k_range[np.argmax(silhouette_scores)]
        st.write(f'Nilai K terbaik berdasarkan Silhouette Score adalah K = {optimal_k}')
        
    # # K-means clustering
    # kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    # kmeans.fit(data_standardized)
        
    # # Menampilkan cluster
    # clusters = pd.DataFrame(kmeans.labels_, columns=['Cluster'])
        
    # # Pastikan data_cleansed tersedia dan memiliki kolom Cluster
    # data_cleansed = st.session_state.df_combined.copy()  # Salin data_cleansed yang sudah dibersihkan
    # data_cleansed['Cluster'] = clusters  # Menambahkan hasil clustering sebagai kolom Cluster
        
    # Simpan hasil clustering ke session state
    # st.session_state.data_cleansed = data_cleansed
        
    # st.subheader('Hasil K-means Clustering')
    # st.dataframe(data_cleansed)
        
    # Evaluasi Silhouette Score
    # silhouette_avg = silhouette_score(data_standardized, kmeans.labels_)
    # st.subheader('Evaluasi Silhouette Score')
    # st.write(f'Silhouette Score untuk K={optimal_k}: {silhouette_avg:.2f}')
        
    # Visualisasi hasil clustering
    # st.subheader('Visualisasi Hasil Clustering')
    # fig, ax = plt.subplots(figsize=(14, 6))
    # sns.scatterplot(x=data_standardized.iloc[:, 0], y=data_standardized.iloc[:, 1], hue=clusters['Cluster'], palette='tab10', ax=ax)
    # st.pyplot(fig)
else:
    st.error("Pengolahan data belum dilakukan. Harap lakukan pengolahan data terlebih dahulu.")
