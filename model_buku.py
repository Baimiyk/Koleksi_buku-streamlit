class Buku:
    def __init__(self, id_buku, judul, penulis, tahun, genre, status="Belum Dibaca"):
        self.id = id_buku
        self.judul = judul
        self.penulis = penulis
        self.tahun = tahun
        self.genre = genre
        self.status = status  # "Belum Dibaca", "Sedang Dibaca", "Selesai"

    def update_status(self, status_baru: str):
        status_valid = ["Belum Dibaca", "Sedang Dibaca", "Selesai"]
        if status_baru in status_valid:
            self.status = status_baru
        else:
            print(f"❌ Status tidak valid: {status_baru}")

    def to_dict(self):
        return {
            "ID": self.id,
            "Judul": self.judul,
            "Penulis": self.penulis,
            "Tahun": self.tahun,
            "Genre": self.genre,
            "Status": self.status
        }

    def __repr__(self):
        return f"Buku(ID={self.id}, Judul='{self.judul}', Status='{self.status}')"
