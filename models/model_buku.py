from config.database import Database


class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    def get_all_buku(self):
        if not self.conn:
            return []

        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(
                f"SELECT * FROM {self.table_name} ORDER BY id_buku"
            )
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()

    def create_buku(self, judul, penulis, tahun_terbit):
        if not self.conn:
            return False

        cursor = None
        try:
            cursor = self.conn.cursor()
            query = (
                f"INSERT INTO {self.table_name} "
                "(judul, penulis, tahun_terbit) VALUES (%s, %s, %s)"
            )
            cursor.execute(query, (judul, penulis, tahun_terbit))
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()

    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        if not self.conn:
            return False

        cursor = None
        try:
            cursor = self.conn.cursor()
            query = (
                f"UPDATE {self.table_name} "
                "SET judul = %s, penulis = %s, tahun_terbit = %s "
                "WHERE id_buku = %s"
            )
            cursor.execute(
                query,
                (judul, penulis, tahun_terbit, id_buku),
            )
            self.conn.commit()

            if cursor.rowcount == 0:
                cursor.execute(
                    f"SELECT id_buku FROM {self.table_name} "
                    "WHERE id_buku = %s",
                    (id_buku,),
                )
                return cursor.fetchone() is not None

            return True
        except Exception:
            self.conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()

    def delete_buku(self, id_buku):
        if not self.conn:
            return False

        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                f"DELETE FROM {self.table_name} WHERE id_buku = %s",
                (id_buku,),
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception:
            self.conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()