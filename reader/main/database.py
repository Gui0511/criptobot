import sqlite3
import os
from datetime import datetime

# Caminho do banco
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "../data/velas.db")

def conectar():
    conn = sqlite3.connect(DB_PATH)
    return conn

def criar_tabela():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS velas (
                moeda TEXT,
                timestamp TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                PRIMARY KEY (moeda, timestamp)
            )
        """)
        conn.commit()

def salvar_velas(moeda, candles):
    with conectar() as conn:
        cursor = conn.cursor()
        for c in candles:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO velas (
                        moeda, timestamp, open, high, low, close, volume
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    moeda,
                    datetime.utcfromtimestamp(c["timestamp"] / 1000).isoformat() + "Z",
                    c["open"],
                    c["high"],
                    c["low"],
                    c["close"],
                    c["volume"]
                ))
            except Exception as e:
                print(f"❌ Erro ao salvar candle de {moeda}: {e}")
        conn.commit()
