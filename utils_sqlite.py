import sqlite3
from model_buku import Buku
from koleksi import KoleksiBuku

NAMA_DB = "data_buku.db"

# --- Membuat koneksi SQLite ---
def get_koneksi():
    return sqlite3.connect(NAMA_DB)

# --- Membuat tabel jika belum ada ---
def setup_database():
    with get_koneksi() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS buku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            penulis TEXT NOT NULL,
            tahun INTEGER,
            genre TEXT,
            status TEXT
        )
        """)
        conn.commit()

# --- Membaca semua buku ke dalam KoleksiBuku ---
def baca_dari_sqlite() -> KoleksiBuku:
    setup_database()
    koleksi = KoleksiBuku()
    with get_koneksi() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buku ORDER BY id")
        for row in cursor.fetchall():
            buku = Buku(row[0], row[1], row[2], row[3], row[4], row[5])
            koleksi.tambah_buku(buku)
    return koleksi

# --- Menyimpan buku baru ---
def simpan_buku_baru(buku: Buku):
    with get_koneksi() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO buku (judul, penulis, tahun, genre, status)
            VALUES (?, ?, ?, ?, ?)
        """, (buku.judul, buku.penulis, buku.tahun, buku.genre, buku.status))
        conn.commit()

# --- Update buku berdasarkan ID ---
def update_buku(buku: Buku):
    with get_koneksi() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE buku SET judul=?, penulis=?, tahun=?, genre=?, status=?
            WHERE id=?
        """, (buku.judul, buku.penulis, buku.tahun, buku.genre, buku.status, buku.id))
        conn.commit()

# --- Hapus buku berdasarkan ID ---
def hapus_buku(id_buku: int):
    with get_koneksi() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM buku WHERE id = ?", (id_buku,))
        conn.commit()

# --- Mendapatkan ID berikutnya (tidak wajib di SQLite, tapi tetap jika ingin konsisten) ---
def get_id_berikutnya(koleksi: KoleksiBuku) -> int:
    if not koleksi.daftar_buku:
        return 1
    id_terakhir = max(b.id for b in koleksi.daftar_buku)
    return id_terakhir + 1
