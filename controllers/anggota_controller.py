from tkinter import messagebox

from models.model_anggota import AnggotaModel
from view.anggota_view import AnggotaView


class AnggotaController:
    def __init__(self):
        self.view = AnggotaView()
        self.model = AnggotaModel()
        self.tampilkan_data_anggota()

    def tampilkan_data_anggota(self):
        tabel = self.view.tabel

        for item in tabel.get_children():
            tabel.delete(item)

        try:
            daftar = self.model.get_all_anggota()

            for anggota in daftar:
                tabel.insert(
                    "",
                    "end",
                    iid=str(anggota["id_anggota"]),
                    values=(
                        anggota["id_anggota"],
                        anggota["nama"],
                        anggota["alamat"],
                    ),
                )
        except Exception as error:
            messagebox.showerror(
                "Gagal Memuat Anggota",
                f"Data anggota tidak dapat dimuat dari MySQL.\n\n{error}",
                parent=self.view,
            )

    def run(self):
        self.view.mainloop()