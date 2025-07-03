import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from model_buku import Buku
from koleksi import KoleksiBuku
from utils_sqlite import (
    baca_dari_sqlite,
    simpan_buku_baru,
    update_buku,
    hapus_buku,
    get_id_berikutnya
)

st.set_page_config(page_title="Koleksi Buku Pribadi (SQLite)", layout="wide")

# ------------------------- SIDEBAR -------------------------
st.sidebar.title("📚 Navigasi")
menu = st.sidebar.radio("Menu", ["Daftar Buku", "Tambah Buku", "Statistik & Rekomendasi"])
st.sidebar.markdown("---")
st.sidebar.caption("Tugas Besar PBO - SQLite Edition")

# ------------------------- DATA KOLEKSI -------------------------
koleksi = baca_dari_sqlite()

# ------------------------- DAFTAR BUKU -------------------------
if menu == "Daftar Buku":
    st.header("📚 Daftar Koleksi Buku")

    df = pd.DataFrame([b.to_dict() for b in koleksi.daftar_buku])

    if df.empty:
        st.warning("Belum ada buku dalam koleksi.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox("Filter Status", ["Semua"] + ["Belum Dibaca", "Sedang Dibaca", "Selesai"])
        with col2:
            genre_filter = st.selectbox("Filter Genre", ["Semua"] + sorted(df["Genre"].unique()))

        if status_filter != "Semua":
            df = df[df["Status"] == status_filter]
        if genre_filter != "Semua":
            df = df[df["Genre"] == genre_filter]

        st.write("### 📋 Daftar Buku")
        for index, row in df.iterrows():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 2, 1.5, 2, 2, 1.5])
            col1.markdown(f"**{row['ID']}**")
            col2.markdown(row["Judul"])
            col3.markdown(row["Penulis"])
            col4.markdown(str(row["Tahun"]))
            col5.markdown(row["Genre"])
            col6.markdown(row["Status"])
            if col7.button("✏️ Edit", key=f"edit_{row['ID']}"):
                st.session_state["edit_id"] = row["ID"]
            if col7.button("🗑️ Hapus", key=f"hapus_{row['ID']}"):
                hapus_buku(row["ID"])
                st.success(f"Buku ID {row['ID']} berhasil dihapus.")
                st.rerun()

        # --- Form Edit jika tombol ditekan ---
        if "edit_id" in st.session_state:
            buku_diedit = next((b for b in koleksi.daftar_buku if b.id == st.session_state["edit_id"]), None)
            if buku_diedit:
                st.markdown("---")
                st.subheader(f"✏️ Edit Buku ID {buku_diedit.id}")
                with st.form("form_edit_buku"):
                    judul_baru = st.text_input("Judul", value=buku_diedit.judul)
                    penulis_baru = st.text_input("Penulis", value=buku_diedit.penulis)
                    tahun_baru = st.number_input("Tahun Terbit", min_value=1000, max_value=2100, value=buku_diedit.tahun)
                    genre_baru = st.text_input("Genre", value=buku_diedit.genre)
                    status_baru = st.selectbox("Status Baca", ["Belum Dibaca", "Sedang Dibaca", "Selesai"], index=["Belum Dibaca", "Sedang Dibaca", "Selesai"].index(buku_diedit.status))

                    simpan = st.form_submit_button("Simpan Perubahan")
                    if simpan:
                        buku_diedit.judul = judul_baru
                        buku_diedit.penulis = penulis_baru
                        buku_diedit.tahun = tahun_baru
                        buku_diedit.genre = genre_baru
                        buku_diedit.status = status_baru

                        update_buku(buku_diedit)
                        del st.session_state["edit_id"]
                        st.success("✅ Data buku berhasil diperbarui.")
                        st.rerun()

# ------------------------- TAMBAH BUKU -------------------------
elif menu == "Tambah Buku":
    st.header("➕ Tambah Buku Baru")

    with st.form("form_tambah"):
        judul = st.text_input("Judul Buku")
        penulis = st.text_input("Penulis")
        tahun = st.number_input("Tahun Terbit", min_value=1000, max_value=2100, step=1)
        genre = st.text_input("Genre (misal: Fiksi, Sains, Sejarah)")
        status = st.selectbox("Status Baca", ["Belum Dibaca", "Sedang Dibaca", "Selesai"])

        submitted = st.form_submit_button("Simpan Buku")

        if submitted:
            if not (judul and penulis and genre):
                st.warning("Isi semua kolom yang wajib.")
            else:
                buku = Buku(None, judul, penulis, tahun, genre, status)
                simpan_buku_baru(buku)
                st.success("Buku berhasil ditambahkan!")
                st.rerun()

# ------------------------- STATISTIK & REKOMENDASI -------------------------
elif menu == "Statistik & Rekomendasi":
    st.header("📊 Statistik Koleksi Buku")

    statistik = koleksi.hitung_statistik()
    st.subheader("Status Bacaan")

    col1, col2 = st.columns([1, 2])
    with col1:
        for k, v in statistik.items():
            st.markdown(f"**{k}**: {v}")
    with col2:
        labels = ["Selesai", "Sedang Dibaca", "Belum Dibaca"]
        sizes = [
            statistik.get("Selesai", 0),
            statistik.get("Sedang Dibaca", 0),
            statistik.get("Belum Dibaca", 0)
        ]

    if sum(sizes) == 0:
        st.info("Belum ada data bacaan untuk ditampilkan dalam grafik.")
    else:
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

    st.divider()
    st.subheader("🎯 Rekomendasi Berdasarkan Genre Favorit")

    rekomendasi = koleksi.rekomendasi_genre()
    if not rekomendasi:
        st.info("Belum ada rekomendasi. Baca beberapa buku dulu!")
    else:
        df_rekom = pd.DataFrame([b.to_dict() for b in rekomendasi])
        st.dataframe(df_rekom, use_container_width=True)
