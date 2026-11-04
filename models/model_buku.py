from config.database import Database

class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    def get_all_buku(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_buku(self, judul, penulis, tahun_terbit):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (judul, penulis, tahun_terbit) VALUES (%s, %s, %s)"
            val = (judul, penulis, tahun_terbit)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()
            return True
        return False

    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"UPDATE {self.table_name} SET judul = %s, penulis = %s, tahun_terbit = %s WHERE id_buku = %s"
            val = (judul, penulis, tahun_terbit, id_buku)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()
            return True
        return False
    
    def delete_buku(self, id_buku):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                # Hapus catatan peminjaman yang terkait dengan buku
                query_peminjaman = """
                    DELETE FROM peminjaman
                    WHERE id_buku = %s
                """
                cursor.execute(query_peminjaman, (id_buku,))

                # Hapus data buku
                query_buku = """
                    DELETE FROM buku
                    WHERE id_buku = %s
                """
                cursor.execute(query_buku, (id_buku,))

                self.conn.commit()
                return True

            except Exception:
                self.conn.rollback()
                raise

            finally:
                cursor.close()

        return False

   