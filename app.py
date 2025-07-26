import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from datetime import datetime

nltk.download('vader_lexicon')

USERNAME = "admin"
PASSWORD = "123"

if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 💻 Login Page
def login():
    st.title("🔐 Login Admin")
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    if st.button("➡️ Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.page = "dashboard"
        else:
            st.error("❌ Username atau password salah!")

# 🏠 Halaman Utama
def home():
    st.title("🏛️ Aplikasi Analisis Sentimen Layanan SAMSAT")
    st.write("👋 Selamat datang! Silakan pilih menu di samping.")

# 💬 Formulir Komentar
def form_page():
    st.title("💬 Formulir Komentar")
    nama = st.text_input("📝 Nama")
    sumber = st.selectbox("🌐 Sumber", ["Instagram", "Google Maps", "YouTube", "Lainnya"])
    pelayanan = st.text_input("🛠️ Pelayanan")
    komentar = st.text_area("💭 Komentar")

    if st.button("📤 Kirim"):
        if komentar.strip() == "":
            st.warning("⚠️ Komentar tidak boleh kosong!")
            return

        sia = SentimentIntensityAnalyzer()
        skor = sia.polarity_scores(komentar)
        if skor['compound'] >= 0.05:
            sentimen = "Positif"
        elif skor['compound'] <= -0.05:
            sentimen = "Negatif"
        else:
            sentimen = "Netral"

        komentar_baru = pd.DataFrame({
            "Tanggal": [datetime.today().strftime('%Y-%m-%d')],
            "Nama": [nama],
            "Sumber": [sumber],
            "Pelayanan": [pelayanan],
            "Komentar": [komentar],
            "Sentimen": [sentimen],
            "Waktu": [datetime.today().strftime('%Y-%m-%d %H:%M:%S')]
        })

        try:
            df_lama = pd.read_csv("data_komentar.csv")
            df_baru = pd.concat([df_lama, komentar_baru], ignore_index=True)
        except:
            df_baru = komentar_baru

        df_baru.to_csv("data_komentar.csv", index=False)
        st.success("✅ Komentar berhasil dikirim!")

# 📊 Dashboard Admin
def dashboard():
    st.title("📊 Dashboard Admin")
    try:
        df = pd.read_csv("data_komentar.csv")
        st.subheader("📈 Distribusi Sentimen")
        st.bar_chart(df["Sentimen"].value_counts())

        st.subheader("☁️ Wordcloud Komentar")
        all_comments = " ".join(df["Komentar"].astype(str))
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_comments)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        st.subheader("🗂️ Data Komentar")
        st.dataframe(df)

        if st.button("🔄 Muat Ulang Dashboard"):
            st.experimental_rerun()

    except Exception as e:
        st.error(f"⚠️ Belum ada data komentar atau terjadi kesalahan: {e}")

# ▶️ Main Program
def main():
    st.sidebar.title("📌 Menu")
    menu = st.sidebar.radio("📂 Navigasi", ["Home", "Formulir Komentar", "Login Admin"])

    if menu == "Home":
        st.session_state.page = "home"
    elif menu == "Formulir Komentar":
        st.session_state.page = "form"
    elif menu == "Login Admin":
        if not st.session_state.logged_in:
            st.session_state.page = "login"
        else:
            st.session_state.page = "dashboard"

    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "form":
        form_page()
    elif st.session_state.page == "login":
        login()
    elif st.session_state.page == "dashboard":
        dashboard()

if __name__ == "__main__":
    main()
