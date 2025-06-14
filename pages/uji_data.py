import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
from yellowbrick.cluster import KElbowVisualizer
from yellowbrick.cluster.elbow import kelbow_visualizer

st.title("Evaluasi Data")
tab1, tab2, tab3 = st.tabs(["Standarization", "Elbow Method", "Silhoutte Score"])
if st.session_state.df_combined is not None:
    with tab1:
        scaler = StandardScaler()
        data_standardized = pd.DataFrame(scaler.fit_transform(st.session_state.df_combined.select_dtypes(include=[np.number])))

        st.session_state.data_standardized = data_standardized
                
        st.subheader('Data Standarisasi')
        st.dataframe(data_standardized)
                
        st.subheader('Scatter Plot Sebelum dan Sesudah Standarisasi')
                
        figu, axes = plt.subplots(1, 2, figsize=(14, 6))
                
        sns.scatterplot(x=st.session_state.df_combined.iloc[:, 0], y=st.session_state.df_combined.iloc[:, 1], ax=axes[0])
        axes[0].set_title('Sebelum Standarisasi')
                
        sns.scatterplot(x=data_standardized.iloc[:, 0], y=data_standardized.iloc[:, 1], ax=axes[1])
        axes[1].set_title('Setelah Standarisasi')
                
        st.pyplot(figu)

        data_standardized = st.session_state.data_standardized
        
    with tab2:
        fig, visualizer = plt.subplots()
        visualizer = KElbowVisualizer(KMeans(), k=(1, 11), distance_metric='euclidean', random_state=42)  
        visualizer.fit(data_standardized)
        visualizer.poof()
        visual = visualizer.ax.figure
        fig.set_size_inches(14, 6)
        st.pyplot(fig)

        
    with tab3:
        k_range = range(2, 11)
        silhouette_scores = []
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(data_standardized)
            silhouette_scores.append(silhouette_score(data_standardized, kmeans.labels_))
            
        k_scores_df = pd.DataFrame({
            'K': k_range,
            'Silhouette Score': silhouette_scores
        })

        st.subheader('Silhouette Score untuk Nilai K (2-10)')
        st.dataframe(k_scores_df)

        fig, ax = plt.subplots()
        ax = kelbow_visualizer(KMeans(random_state=42), data_standardized, k=(2,11), metric='silhouette',distance_metric='euclidean', timings=False)

        fig.set_size_inches(14, 6)
        st.pyplot(fig)

        # Pilih K terbaik
        optimal_k = k_range[np.argmax(silhouette_scores)]
        optimal_nilai = k_scores_df['Silhouette Score'].max()
        st.write(f'Nilai K terbaik berdasarkan Silhouette Score adalah K = {optimal_k}, dengan nilai {optimal_nilai}')
        st.write(f'Disarankan untuk menggunakan nilai K = {optimal_k} dalam penentuan jumlah cluster.')
else:
    st.error("Pengolahan data belum dilakukan. Harap lakukan pengolahan data terlebih dahulu.")
