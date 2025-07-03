from model_buku import Buku

class KoleksiBuku:
    def __init__(self):
        self.daftar_buku = []

    def tambah_buku(self, buku: Buku):
        if isinstance(buku, Buku):
            self.daftar_buku.append(buku)
        else:
            print("❌ Objek yang ditambahkan bukan instance dari Buku")

    def cari_buku(self, kata_kunci: str):
        hasil = []
        kata_kunci = kata_kunci.lower()
        for buku in self.daftar_buku:
            if kata_kunci in buku.judul.lower() or kata_kunci in buku.penulis.lower():
                hasil.append(buku)
        return hasil

    def filter_status(self, status: str):
        return [b for b in self.daftar_buku if b.status == status]

    def filter_genre(self, genre: str):
        return [b for b in self.daftar_buku if b.genre.lower() == genre.lower()]

    def update_status_buku(self, id_buku: int, status_baru: str):
        for buku in self.daftar_buku:
            if buku.id == id_buku:
                buku.update_status(status_baru)
                return True
        return False

    def hitung_statistik(self):
        total = len(self.daftar_buku)
        selesai = len([b for b in self.daftar_buku if b.status == "Selesai"])
        sedang = len([b for b in self.daftar_buku if b.status == "Sedang Dibaca"])
        belum = len([b for b in self.daftar_buku if b.status == "Belum Dibaca"])

        return {
            "Total Buku": total,
            "Selesai": selesai,
            "Sedang Dibaca": sedang,
            "Belum Dibaca": belum
        }

    def rekomendasi_genre(self, max_rekomendasi=3):
        genre_count = {}
        for buku in self.daftar_buku:
            if buku.status == "Selesai":
                genre = buku.genre
                genre_count[genre] = genre_count.get(genre, 0) + 1
        if not genre_count:
            return []

        genre_teratas = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
        genre_favorit = [g[0] for g in genre_teratas[:max_rekomendasi]]

        # Ambil buku dengan genre tersebut dan status belum dibaca
        rekomendasi = []
        for g in genre_favorit:
            rekomendasi.extend([b for b in self.daftar_buku if b.genre == g and b.status != "Selesai"])
        return rekomendasi