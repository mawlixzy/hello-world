import pandas as pd
matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
from PIL import Image



#Menampilkan logo
st.header('Moli Hijabi')
logo_path = 'Moli.png'  
logo = Image.open(logo_path)

#Menampilkan Judul
st.title('E-Commerce Performance Analysis')


merged_data = pd.read_csv('merged_data.csv')


tab1, tab2 = st.tabs (["Sales Trend Analysis", "Rating Bar"])

with tab1:
    ## PLOT GRAFIK SALES TREND ANALYSIS
    # Fungsi untuk memproses data setelah file dibaca
    def process_and_plot_data(merged_data):
        # Daftar kolom datetime
        datetime_columns = [
            'order_purchase_timestamp_x',
            'order_delivered_customer_date_x',
            'order_estimated_delivery_date_x'
        ]
        
        # Mengonversi kolom menjadi tipe datetime 
        for column in datetime_columns:
            merged_data[column] = pd.to_datetime(merged_data[column], errors='coerce')

        # Memeriksa nilai yang hilang
        missing_values = merged_data[datetime_columns].isna().sum()

        # Menghapus baris yang memiliki nilai datetime yang hilang (NaN)
        merged_data = merged_data.dropna(subset=datetime_columns)

        # Membuat kolom baru dengan format periode bulanan
        merged_data['order_purchase_month_x'] = merged_data['order_purchase_timestamp_x'].dt.to_period('M')
        
        # Menghitung jumlah pesanan per bulan
        monthly_sales = merged_data.groupby('order_purchase_month_x').size()
        
        # Plotting grafik trend penjualan
        fig, ax = plt.subplots(figsize=(10, 5))
        monthly_sales.plot(kind='line', marker='o', linestyle='-', color='black', linewidth=2, markersize=6, label='Sales', ax=ax)
        ax.set_title('Sales Trend Analysis', fontsize=20, fontweight='bold', color='darkblue')
        ax.set_xlabel('Month', fontsize=10, fontweight='bold')
        ax.set_ylabel('Number of Orders', fontsize=10, fontweight='bold')
        ax.grid(True)
        
        st.pyplot(fig)
        st.write("Sales Trend Analysis Graphic")
        st.caption("The number of orders shows a trend of increasing month by month. There is a significant spike around October 2017; however, there are some fluctuations in the number of orders in 2018, with several months showing a decline. This indicates instability in sales that may need to be addressed. Despite the fluctuations, there is a long-term trend indicating that the total number of orders remains higher at the end of the observation period compared to the beginning. This suggests that, despite challenges, the business may have successfully expanded its customer base and improved customer loyalty.")

    # Baca file CSV dari folder lokal (tanpa file uploader)
    # Misalnya file CSV ada di folder yang sama dengan script, atau di subfolder 'data'
    csv_file_path = 'merged_data.csv'  # Ganti dengan path sesuai lokasi file CSV kamu

    # Memproses dan membuat plot
    process_and_plot_data(merged_data)

with tab2:
    ## PLOT GRAFIK RATING CUSTOMERS
    # Membuat plot
    fig = plt.figure(figsize=(10, 5))
    sns.countplot(data=merged_data, x='review_score', color='black')
    plt.title('Distribution of Review Scores', fontsize=18, fontweight='bold', color='darkblue')
    plt.xlabel('Review Score', fontsize=14, fontweight='bold')
    plt.ylabel('Count', fontsize=14, fontweight='bold')

    # Menampilkan plot di Streamlit
    st.write("")
    st.pyplot(fig)
    st.write("Our Rating Bar")
    st.caption("It can be seen that the majority of reviews have high scores, especially a score of 5. This indicates that customers are generally satisfied with the products or services provided, reflecting good quality or a consistently positive experience.")
    st.write("")
    st.write("")

with st.sidebar:
    st.title('Moli Hijabi')
    st.write('Comfy Your Hijabi with Moli!')
    st.image(logo, width=200) 
    text = st.text_area('Feedback')
    st.write('Feedback: ', text)

st.write("")
st.write("")
st.write ('Rate this web')
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You rated this web {sentiment_mapping[selected]} star(s).")
