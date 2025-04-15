import cx_Oracle
import os

# Ruta al cliente Oracle Instant Client (ubicado en el Escritorio)
oracle_client_path = r"C:\Users\negre\OneDrive\Escritorio\oracle\instantclient_21_17"
os.add_dll_directory(oracle_client_path)

# Inicializa el cliente Oracle
cx_Oracle.init_oracle_client(lib_dir=oracle_client_path)

# Ruta al wallet (ubicado en el Escritorio en la carpeta oraclewallet)
os.environ["TNS_ADMIN"] = r"C:\Users\negre\OneDrive\Escritorio\oraclewallet"



