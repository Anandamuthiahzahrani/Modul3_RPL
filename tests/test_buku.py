from unittest.mock import MagicMock, patch
from models.buku_model import BukuModel


def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True
    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()
    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()

def test_get_all_buku():
    # Membuat koneksi dan cursor tiruan
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Data buku tiruan
    data_buku = [
        {
            "id_buku": 1,
            "judul": "Pemrograman Python",
            "penulis": "Andi",
            "tahun_terbit": 2024
        }
    ]

    mock_cursor.fetchall.return_value = data_buku
    mock_conn.cursor.return_value = mock_cursor

    # Menggantikan koneksi database dengan mock
    with patch("models.buku_model.Database") as mock_database:
        mock_database.return_value.get_connection.return_value = mock_conn

        model = BukuModel()
        hasil = model.get_all_buku()

    # Memastikan data yang dikembalikan sesuai
    assert hasil == data_buku

    # Memastikan query dijalankan
    mock_cursor.execute.assert_called_once_with("SELECT * FROM buku")

    # Memastikan cursor ditutup
    mock_cursor.close.assert_called_once()
