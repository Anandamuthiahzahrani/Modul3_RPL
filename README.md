# Sistem Manajemen Perpustakaan

Aplikasi desktop untuk mengelola data buku dan anggota perpustakaan. Aplikasi dibuat dengan Python, CustomTkinter, dan MySQL. Login membedakan pengguna admin dan anggota.

## Struktur Direktori

```text
config/       Konfigurasi koneksi MySQL
controllers/  Logika aplikasi dan penghubung model dengan tampilan
models/       Akses dan pengelolaan data
view/         Tampilan aplikasi
tests/        Unit test
main.py       Titik masuk aplikasi
```

## Instalasi dan Konfigurasi Database

1. Nyalakan MySQL melalui Laragon.
2. Buat database dan tabel yang digunakan aplikasi:

```sql
CREATE DATABASE perpustakaan;
USE perpustakaan;

CREATE TABLE users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'anggota') NOT NULL DEFAULT 'anggota'
);

CREATE TABLE buku (
    id_buku INT AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(255) NOT NULL,
    penulis VARCHAR(255) NOT NULL,
    tahun_terbit INT NOT NULL
);

CREATE TABLE anggota (
    id_anggota INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    alamat VARCHAR(255) NOT NULL
);

CREATE TABLE peminjaman (
    id_peminjaman INT AUTO_INCREMENT PRIMARY KEY,
    id_buku INT NOT NULL,
    FOREIGN KEY (id_buku) REFERENCES buku(id_buku)
);

INSERT INTO users (username, password, role)
VALUES
    ('petugas', SHA2('admin123', 256), 'admin'),
    ('mahasiswa', SHA2('user123', 256), 'anggota');
```

3. Periksa pengaturan host, nama database, username, dan password MySQL di `config/database.py`. Nilai awal proyek: `localhost`, database `perpustakaan`, user `root`, password kosong.

## Cara Menjalankan

```powershell
pip install -r requirements.txt
python main.py
```

Pastikan MySQL Laragon menyala sebelum membuka aplikasi.