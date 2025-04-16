import cx_Oracle
import os
import platform

sistema = platform.system()

#Se agrega if para evitar conflictos al usar mac os o windows.
if sistema == 'Windows':
    # Ruta en Windows
    oracle_client_path = r"C:\Users\negre\OneDrive\Escritorio\oracle\instantclient_21_17"
    os.add_dll_directory(oracle_client_path)
    cx_Oracle.init_oracle_client(lib_dir=oracle_client_path)

    # Ruta al wallet en Windows
    os.environ["TNS_ADMIN"] = r"C:\Users\negre\OneDrive\Escritorio\oraclewallet"

elif sistema == 'Darwin':  # macOS
    # Ruta en macOS (ajústala según dónde tengas el Instant Client)
    oracle_client_path = "/Users/dani/Oracle/client/instantclient_23_1"
    cx_Oracle.init_oracle_client(lib_dir=oracle_client_path)

    # Ruta al wallet en macOS (ajústala también)
    os.environ["TNS_ADMIN"] = "/Users/dani/Oracle/wallet"
