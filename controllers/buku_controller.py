from tkinter import messagebox
from models.model_buku import BukuModel
from view.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding tombol simpan
        self.view.btn_simpan.configure(command=self.simpan_data)

        # OTORISASI: Jika bukan admin, nonaktifkan form input dan tombol simpan
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (khusus Admin)")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    buku['id_buku'],
                    buku['judul'],
                    buku['penulis'],
                    buku['tahun_terbit'],
                ),
            )

    def simpan_data(self):
        # Proteksi ganda di Level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def run(self):
        self.view.mainloop()

    def ambil_input_form(self):
        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun_teks = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun_teks:
            messagebox.showwarning(
                "Data belum lengkap",
                "Judul, nama penulis, dan tahun terbit harus diisi.",
                parent=self.view,
            )
            return None

        try:
            tahun = int(tahun_teks)
            if tahun < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Tahun tidak valid",
                "Tahun terbit harus berupa angka tahun yang valid.",
                parent=self.view,
            )
            return None

        return judul, penulis, tahun

    def tampilkan_data_buku(self):
        tabel = self.view.tabel

        # Kosongkan isi tabel sebelum memuat ulang data.
        for item in tabel.get_children():
            tabel.delete(item)

        try:
            daftar_buku = self.model.get_all_buku()

            for buku in daftar_buku:
                id_buku = buku.get("id_buku")
                judul = buku.get("judul", "")
                penulis = buku.get("penulis", "")
                tahun = buku.get("tahun_terbit", "")

                tabel.insert(
                    "",
                    "end",
                    iid=str(id_buku),
                    values=(id_buku, judul, penulis, tahun),
                )

        except Exception as error:
            messagebox.showerror(
                "Gagal Memuat Data",
                f"Data buku tidak dapat dimuat.\n\nDetail: {error}",
                parent=self.view,
            )

    def simpan_data(self):
        data = self.ambil_input_form()
        if data is None:
            return

        try:
            berhasil = self.model.create_buku(*data)

            if berhasil:
                self.tampilkan_data_buku()
                self.bersihkan_form()

                messagebox.showinfo(
                    "Berhasil",
                    "Data buku berhasil disimpan.",
                    parent=self.view,
                )
            else:
                messagebox.showerror(
                    "Gagal Menyimpan",
                    "Data tidak dapat disimpan. Periksa koneksi database.",
                    parent=self.view,
                )

        except Exception as error:
            messagebox.showerror(
                "Gagal Menyimpan",
                f"Data buku gagal disimpan.\n\nDetail: {error}",
                parent=self.view,
            )

    def pilih_buku(self, _event=None):
        pilihan = self.view.tabel.selection()

        if not pilihan:
            self.id_buku_terpilih = None
            return

        nilai_baris = self.view.tabel.item(
            pilihan[0],
            "values",
        )

        if not nilai_baris:
            return

        self.id_buku_terpilih = int(nilai_baris[0])

        self.view.entry_judul.delete(0, "end")
        self.view.entry_judul.insert(0, nilai_baris[1])

        self.view.entry_penulis.delete(0, "end")
        self.view.entry_penulis.insert(0, nilai_baris[2])

        self.view.entry_tahun.delete(0, "end")
        self.view.entry_tahun.insert(0, nilai_baris[3])

    def perbarui_data(self):
        if self.id_buku_terpilih is None:
            messagebox.showwarning(
                "Pilih Buku",
                "Klik baris buku pada tabel yang ingin diperbarui.",
                parent=self.view,
            )
            return

        data = self.ambil_input_form()
        if data is None:
            return

        try:
            berhasil = self.model.update_buku(
                self.id_buku_terpilih,
                *data,
            )

            if berhasil:
                self.tampilkan_data_buku()
                self.bersihkan_form()

                messagebox.showinfo(
                    "Berhasil",
                    "Data buku berhasil diperbarui.",
                    parent=self.view,
                )
            else:
                messagebox.showwarning(
                    "Data Tidak Berubah",
                    "Buku tidak ditemukan atau nilainya tidak berubah.",
                    parent=self.view,
                )

        except Exception as error:
            messagebox.showerror(
                "Gagal Memperbarui",
                f"Data buku gagal diperbarui.\n\nDetail: {error}",
                parent=self.view,
            )

    def hapus_data(self):
        if self.id_buku_terpilih is None:
            messagebox.showwarning(
                "Pilih Buku",
                "Klik baris buku pada tabel yang ingin dihapus.",
                parent=self.view,
            )
            return

        setuju = messagebox.askyesno(
            "Konfirmasi Hapus",
            "Yakin ingin menghapus buku yang dipilih?",
            parent=self.view,
        )

        if not setuju:
            return

        try:
            berhasil = self.model.delete_buku(
                self.id_buku_terpilih,
            )

            if berhasil:
                self.tampilkan_data_buku()
                self.bersihkan_form()

                messagebox.showinfo(
                    "Berhasil",
                    "Data buku berhasil dihapus.",
                    parent=self.view,
                )
            else:
                messagebox.showwarning(
                    "Data Tidak Ditemukan",
                    "Data buku tersebut tidak ditemukan.",
                    parent=self.view,
                )

        except Exception as error:
            messagebox.showerror(
                "Gagal Menghapus",
                f"Data buku gagal dihapus.\n\nDetail: {error}",
                parent=self.view,
            )

    def bersihkan_form(self):
        self.id_buku_terpilih = None

        self.view.entry_judul.delete(0, "end")
        self.view.entry_penulis.delete(0, "end")
        self.view.entry_tahun.delete(0, "end")

        pilihan = self.view.tabel.selection()
        if pilihan:
            self.view.tabel.selection_remove(*pilihan)


if __name__ == "__main__":
    controller = BukuController()
    controller.run()