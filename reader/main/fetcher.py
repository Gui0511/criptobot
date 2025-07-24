import requests
import time

BASE_URL = "https://api.binance.com"

def get_candles(symbol, interval, limit=1000):
    """
    Busca candles do par especificado com limite e intervalo.
    Retorna lista de dicionários com OHLCV.
    """
    endpoint = f"{BASE_URL}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        candles = []
        for item in data:
            candles.append({
                "timestamp": item[0],
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5])
            })

        return candles

    except Exception as e:
        print(f"❌ Erro ao buscar candles de {symbol}: {e}")
        return []

def get_all_candles(config, limit=1000):
    """
    Busca os candles de todas as moedas configuradas.
    Retorna um dicionário: { "BTCUSDT": [...], "ETHUSDT": [...] }
    """
    interval = config["geral"]["interval"]
    moedas = config["geral"]["coin"]
    resultado = {}

    for symbol in moedas:
        print(f"🔄 Buscando candles de {symbol}...")
        candles = get_candles(symbol, interval, limit)
        resultado[symbol] = candles
        time.sleep(0.2)  # pra não abusar da API da Binance

    return resultado
