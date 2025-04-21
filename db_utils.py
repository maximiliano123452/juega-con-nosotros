from decouple import config
import cx_Oracle
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class OracleDB:
    def __init__(self):
        self.dsn = config("DB_DSN")  # g4db_low
        self.username = config("DB_USERNAME")
        self.password = config("DB_PASSWORD")

    def connect(self) -> Optional[cx_Oracle.Connection]:
        """Conectar usando configuración de wallet_g4db"""
        try:
            conn = cx_Oracle.connect(
                user=self.username,
                password=self.password,
                dsn=self.dsn,
                encoding="UTF-8"
            )
            logger.info(f"Conectado a Oracle {conn.version} (DSN: {self.dsn})")
            return conn
        except cx_Oracle.DatabaseError as e:
            logger.error(f"Conexión fallida {self.dsn}: {e}")
            return None

    # Context manager support
    def __enter__(self):
        self.conn = self.connect()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()