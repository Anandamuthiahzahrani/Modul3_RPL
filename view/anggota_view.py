import customtkinter as ctk
from tkinter import ttk


class AnggotaView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi jendela
        self.title("Sistem Manajemen Perpustakaan - Data Anggota")
        self.geometry("800x450")

        # Konfigurasi grid utama
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # FRAME KIRI: FORM DATA ANGGOTA
        # ==========================================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew"
        )

        ctk.CTkLabel(
            self.frame_kiri,
            text="Form Data Anggota",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Input nama anggota
        self.entry_nama = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Nama Anggota"
        )
        self.entry_nama.pack(
            pady=10, padx=15, fill="x"
        )

        # Input alamat anggota
        self.entry_alamat = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Alamat"
        )
        self.entry_alamat.pack(
            pady=10, padx=15, fill="x"
        )

        # Tombol simpan
        self.btn_simpan = ctk.CTkButton(
            self.frame_kiri,
            text="Simpan Data",
            fg_color="green",
            command=self.simpan_data
        )
        self.btn_simpan.pack(
            pady=(20, 10), padx=15, fill="x"
        )

        # Tombol bersihkan
        self.btn_bersihkan = ctk.CTkButton(
            self.frame_kiri,
            text="Bersihkan Form",
            fg_color="gray",
            command=self.bersihkan_form
        )
        self.btn_bersihkan.pack(
            pady=10, padx=15, fill="x"
        )

        # ==========================================
        # FRAME KANAN: TABEL DATA ANGGOTA
        # ==========================================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(
            row=0, column=1, padx=10, pady=10, sticky="nsew"
        )

        ctk.CTkLabel(
            self.frame_kanan,
            text="Daftar Anggota",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Kolom tabel
        kolom = ("nama", "alamat")

        self.tabel = ttk.Treeview(
            self.frame_kanan,
            columns=kolom,
            show="headings",
            height=15
        )

        # Judul kolom
        self.tabel.heading("nama", text="Nama Anggota")
        self.tabel.heading("alamat", text="Alamat")

        # Lebar kolom
        self.tabel.column(
            "nama", width=150, anchor="w"
        )
        self.tabel.column(
            "alamat", width=250, anchor="w"
        )

        self.tabel.pack(
            fill="both", expand=True, padx=15, pady=10
        )

    # ==========================================
    # FUNGSI SIMPAN DATA KE TABEL
    # ==========================================
    def simpan_data(self):
        nama = self.entry_nama.get().strip()
        alamat = self.entry_alamat.get().strip()

        if nama and alamat:
            self.tabel.insert(
                "", "end", values=(nama, alamat)
            )
            self.bersihkan_form()

    # ==========================================
    # FUNGSI MEMBERSIHKAN FORM
    # ==========================================
    def bersihkan_form(self):
        self.entry_nama.delete(0, "end")
        self.entry_alamat.delete(0, "end")


# Menjalankan aplikasi
if __name__ == "__main__":
    app = AnggotaView()
    app.mainloop()