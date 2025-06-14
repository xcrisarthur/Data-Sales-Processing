import pandas as pd
import streamlit as st

# Fungsi untuk mengelompokkan customer
def kelompokan(customer_name):
    kelompok_a = [
        "RS HERMINA JATINEGARA", "RS HERMINA PODOMORO", "RS HERMINA KEMAYORAN",
        "RS HERMINA DEPOK", "RS HERMINA DAAN MOGOT", "RS HERMINA BOGOR",
        "RS HERMINA CIAWI", "RS HERMINA PIK DUA", "PT. AAM JK2", 
        "PT. MEDIKA LOKA MANAJEMEN - Hermina", "PT. BERSIH AMAN CEMERLANG", 
        "PT. Pembangun Pemilik Pengelola Menara Proteksi Indonesia (PT. P3MPI)", 
        "INSTITUT KESEHATAN HERMINA", "PERKUMPULAN HERMINA GROUP", 
        "PT CAHAYA BALLROOM KEMAYORAN", "PT INTEGRASI BISNIS DIGITAL", 
        "KOPERASI HERMINA PODOMORO", "KOKARMINA PUSAT", "CIPUTRA HOSPITAL CITRAGARDEN CITY"
    ]
    kelompok_b = [
        "KOKARMINA CIRUAS", "KOKARMINA BEKASI", "KOKARMINA GRANDWISATA", 
        "RS HERMINA ARCAMANIK", "RS HERMINA BALIKPAPAN", "RS HERMINA BANYUMANIK",
        "RS HERMINA BEKASI"
    ]
    
    if customer_name in kelompok_a:
        return 'Lius'
    elif customer_name in kelompok_b:
        return 'Eva'
    else:
        return 'Lainnya'

# Membaca file CSV atau Excel yang diunggah
def upload_file():
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Periksa apakah kolom 'Total amount' ada, jika tidak, cari 'jumlah total'
        if 'Total amount' in df.columns:
            total_amount_column = 'Total amount'
        elif 'jumlah total' in df.columns:
            total_amount_column = 'jumlah total'
        else:
            st.error("Kolom 'Total amount' atau 'jumlah total' tidak ditemukan.")
            return None

        # Periksa apakah kolom 'Customer name' ada, jika tidak, cari 'nama pelanggan'
        if 'Customer name' in df.columns:
            customer_name_column = 'Customer name'
        elif 'nama pelanggan' in df.columns:
            customer_name_column = 'nama pelanggan'
        else:
            st.error("Kolom 'Customer name' atau 'nama pelanggan' tidak ditemukan.")
            return None

        # Pemrosesan data
        df[total_amount_column] = df[total_amount_column].replace({'Rp ': '', ',': ''}, regex=True)
        df[total_amount_column] = pd.to_numeric(df[total_amount_column])

        df['Kelompok'] = df[customer_name_column].apply(kelompokan)
        df_grouped = df.groupby(['Kelompok', customer_name_column])[total_amount_column].sum().reset_index()
        df_grouped = df_grouped.rename(columns={'Kelompok': 'Nama Sales'})

        return df_grouped
    return None

# Menampilkan hasil
def main():
    st.title("Data Sales Processing")

    df_grouped = upload_file()

    if df_grouped is not None:
        st.subheader("Processed Data")
        st.write(df_grouped)

        # Menyediakan opsi untuk mendownload hasilnya
        st.download_button(
            label="Download Processed Data",
            data=df_grouped.to_csv(index=False),
            file_name="processed_sales_data.csv",
            mime="text/csv"
        )
        
if __name__ == "__main__":
    main()
