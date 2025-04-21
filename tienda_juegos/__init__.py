import os
import platform
import cx_Oracle
import logging
from pathlib import Path

# Configuración logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_oracle_client():
    """Iniciar Oracle client con wallet_g4db"""
    try:
        # 1. Configurar Client Path
        oracle_client_path = os.getenv('ORACLE_CLIENT_PATH')
        if not oracle_client_path:
            raise ValueError("ORACLE_CLIENT_PATH variable de entorno no establecida")

        if platform.system() == "Windows":
            os.add_dll_directory(oracle_client_path)

        cx_Oracle.init_oracle_client(lib_dir=oracle_client_path)
        logger.info(f"Oracle client inició en: {oracle_client_path}")

        # 2. Configurar Wallet (wallet_g4db)
        wallet_path = Path(os.getenv('TNS_ADMIN', './wallet_g4db')).resolve()
        if not wallet_path.exists():
            raise FileNotFoundError(f"Directorio de wallet no encontrado: {wallet_path}")

        os.environ["TNS_ADMIN"] = str(wallet_path)
        logger.info(f"Oracle wallet configurado en: {wallet_path}")

    except Exception as e:
        logger.error(f"Inicio de Oracle fallido: {str(e)}")
        raise

# Iniciar cuando module es importado
initialize_oracle_client()