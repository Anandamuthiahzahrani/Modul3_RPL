import customtkinter as ctk
from tkinter import ttk


class BukuView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("1000x650")
        self.minsize(850, 500)

        # Konfigurasi grid utama: form kiri dan tabel kanan
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Frame kiri: formulir buku
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew",
        )

        ctk.CTkLabel(
            self.frame_kiri,
            text="Form Data Buku",
            font=("Arial", 20, "bold"),
        ).pack(pady=20)

        # Input judul
        self.entry_judul = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Judul Buku",
        )
        self.entry_judul.pack(
            pady=10,
            padx=15,
            fill="x",
        )

        # Input penulis
        self.entry_penulis = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Nama Penulis",
        )
        self.entry_penulis.pack(
            pady=10,
            padx=15,
            fill="x",
        )

        # Input tahun terbit
        self.entry_tahun = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Tahun Terbit (Misal: 2024)",
        )
        self.entry_tahun.pack(
            pady=10,
            padx=15,
            fill="x",
        )

        # Tombol simpan
        self.btn_simpan = ctk.CTkButton(
            self.frame_kiri,
            text="Simpan Data",
            fg_color="green",
            hover_color="darkgreen",
        )
        self.btn_simpan.pack(
            pady=(20, 10),
            padx=15,
            fill="x",
        )

        # Tombol perbarui
        self.btn_update = ctk.CTkButton(
            self.frame_kiri,
            text="Perbarui Data (Update)",
            fg_color="blue",
            hover_color="darkblue",
        )
        self.btn_update.pack(
            pady=10,
            padx=15,
            fill="x",
        )

        # Tombol hapus
        self.btn_hapus = ctk.CTkButton(
            self.frame_kiri,
            text="Hapus Data (Delete)",
            fg_color="red",
            hover_color="darkred",
        )
        self.btn_hapus.pack(
            pady=10,
            padx=15,
            fill="x",
        )

        # Tombol log out
        self.btn_logout = ctk.CTkButton(
            self.frame_kiri,
            text="Log Out",
            fg_color="gray",
        )
        self.btn_logout.pack(
            side="bottom",
            pady=15,
            padx=15,
            fill="x",
        )

        # Frame kanan: daftar buku
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew",
        )

        ctk.CTkLabel(
            self.frame_kanan,
            text="Daftar Koleksi Buku",
            font=("Arial", 20, "bold"),
        ).pack(pady=20)

        # Tabel buku
        kolom = ("id", "judul", "penulis", "tahun")

        self.tabel = ttk.Treeview(
            self.frame_kanan,
            columns=kolom,
            show="headings",
            height=15,
        )

        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("tahun", text="Tahun")

        self.tabel.column("id", width=50, anchor="center")
        self.tabel.column("judul", width=220)
        self.tabel.column("penulis", width=180)
        self.tabel.column("tahun", width=80, anchor="center")

        self.tabel.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15),
        )


if __name__ == "__main__":
    app = BukuView()
    app.mainloop()