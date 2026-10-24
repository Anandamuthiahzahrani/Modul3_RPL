from models.model_buku import BukuModel

model = BukuModel()

# 1. Menguji Fungsi Create (menambahkan buku baru)
print("Menambahkan data buku...")
model.create_buku("Pemrograman Python MVC", "Guido van Rossum", 2023)
print("Data berhasil disimpan ke Laragon MySQL!")

# 2. Menguji Fungsi Read (menampilkan data)
print("\n=== Data Buku ===")
data_buku = model.get_all_buku()
for buku in data_buku:
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")