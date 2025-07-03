import sqlite3

DB_NAME = "data_buku.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
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


    contoh_data = [
        ("Laskar Pelangi", "Andrea Hirata", 2005, "Fiksi", "Selesai"),
        ("Sapiens", "Yuval Noah Harari", 2011, "Sejarah", "Belum Dibaca"),
        ("Atomic Habits", "James Clear", 2018, "Pengembangan Diri", "Sedang Dibaca")
    ]

    for judul, penulis, tahun, genre, status in contoh_data:
        cursor.execute("SELECT COUNT(*) FROM buku WHERE judul = ?", (judul,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO buku (judul, penulis, tahun, genre, status)
                VALUES (?, ?, ?, ?, ?)
            """, (judul, penulis, tahun, genre, status))

    conn.commit()
    conn.close()
    print("✅ Database berhasil dibuat atau diperbarui.")

if __name__ == "__main__":
    setup_database()
