from tkinter import messagebox

from models.model_buku import BukuModel
from view.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()
        self.id_buku_terpilih = None

        self.view.title(
            f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}"
        )

        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_hapus.configure(command=self.delete_data)
        self.view.btn_logout.configure(command=self.logout)

        self.view.tabel.bind(
            "<<TreeviewSelect>>",
            self.pilih_buku,
        )

        if self.user_role != "admin":
            self.view.btn_simpan.configure(
                state="disabled",
                text="Akses Terkunci (khusus Admin)",
            )
            self.view.btn_update.configure(state="disabled")
            self.view.btn_hapus.configure(state="disabled")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        try:
            data_buku = self.model.get_all_buku()

            for buku in data_buku:
                self.view.tabel.insert(
                    "",
                    "end",
                    values=(
                        buku["id_buku"],
                        buku["judul"],
                        buku["penulis"],
                        buku["tahun_terbit"],
                    ),
                )
        except Exception as error:
            messagebox.showerror(
                "Gagal Memuat Data",
                f"Data buku tidak dapat dimuat.\n\nDetail: {error}",
                parent=self.view,
            )

    def pilih_buku(self, _event=None):
        pilihan = self.view.tabel.selection()

        if not pilihan:
            self.id_buku_terpilih = None
            return

        nilai_baris = self.view.tabel.item(pilihan[0], "values")

        if not nilai_baris:
            return

        self.id_buku_terpilih = int(nilai_baris[0])

        if self.user_role == "admin":
            self.view.entry_judul.delete(0, "end")
            self.view.entry_judul.insert(0, nilai_baris[1])

            self.view.entry_penulis.delete(0, "end")
            self.view.entry_penulis.insert(0, nilai_baris[2])

            self.view.entry_tahun.delete(0, "end")
            self.view.entry_tahun.insert(0, nilai_baris[3])

    def ambil_input_form(self):
        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun_teks = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun_teks:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "Semua kolom form harus diisi.",
                parent=self.view,
            )
            return None

        try:
            tahun = int(tahun_teks)
            if tahun < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Tahun Tidak Valid",
                "Tahun terbit harus berupa angka tahun yang valid.",
                parent=self.view,
            )
            return None

        return judul, penulis, tahun

    def simpan_data(self):
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk menambah data.",
                parent=self.view,
            )
            return

        data = self.ambil_input_form()
        if data is None:
            return

        try:
            if self.model.create_buku(*data):
                self.muat_data_tabel()
                self.bersihkan_form()
                messagebox.showinfo(
                    "Sukses",
                    "Data buku berhasil disimpan!",
                    parent=self.view,
                )
        except Exception as error:
            messagebox.showerror(
                "Gagal Menyimpan",
                f"Data buku gagal disimpan.\n\nDetail: {error}",
                parent=self.view,
            )

    def update_data(self):
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk mengubah data.",
                parent=self.view,
            )
            return

        if self.id_buku_terpilih is None:
            messagebox.showwarning(
                "Pilih Buku",
                "Klik baris buku yang ingin diperbarui terlebih dahulu.",
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
                self.muat_data_tabel()
                self.bersihkan_form()
                messagebox.showinfo(
                    "Sukses",
                    "Data buku berhasil diperbarui!",
                    parent=self.view,
                )
        except Exception as error:
            messagebox.showerror(
                "Gagal Memperbarui",
                f"Data buku gagal diperbarui.\n\nDetail: {error}",
                parent=self.view,
            )

    def delete_data(self):
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk menghapus data.",
                parent=self.view,
            )
            return

        if self.id_buku_terpilih is None:
            messagebox.showwarning(
                "Pilih Buku",
                "Klik baris buku yang ingin dihapus terlebih dahulu.",
                parent=self.view,
            )
            return

        setuju = messagebox.askyesno(
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus data ini?",
            parent=self.view,
        )

        if not setuju:
            return

        try:
            berhasil = self.model.delete_buku(self.id_buku_terpilih)

            if berhasil:
                self.muat_data_tabel()
                self.bersihkan_form()
                messagebox.showinfo(
                    "Sukses",
                    "Data buku berhasil dihapus!",
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

    def logout(self):
        self.view.destroy()

        from controllers.auth_controller import AuthController

        AuthController().run()

    def run(self):
        self.view.mainloop()