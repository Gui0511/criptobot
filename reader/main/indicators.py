import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD, SMAIndicator
from ta.volume import VolumeWeightedAveragePrice

def calcular_indicadores(candles, config_alertas, indicadores_ativos):
    """
    Recebe uma lista de candles (dicionários) e calcula os indicadores ativados.
    Retorna um dicionário com os valores mais recentes.
    """
    df = pd.DataFrame(candles)

    # Garantir colunas certas
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    resultado = {}

    # RSI
    if indicadores_ativos.get("usar_rsi") and config_alertas["rsi"]["ativar"]:
        rsi = RSIIndicator(close=df["close"], window=config_alertas["rsi"]["periodo"])
        resultado["rsi"] = rsi.rsi().iloc[-1]

    # MACD
    if indicadores_ativos.get("usar_macd") and config_alertas["macd"]["ativar"]:
        macd = MACD(close=df["close"],
                    window_fast=config_alertas["macd"]["fast"],
                    window_slow=config_alertas["macd"]["slow"],
                    window_sign=config_alertas["macd"]["signal"])
        resultado["macd_line"] = macd.macd().iloc[-1]
        resultado["macd_signal"] = macd.macd_signal().iloc[-1]
        resultado["macd_hist"] = macd.macd_diff().iloc[-1]

    # MMS
    if indicadores_ativos.get("usar_mms") and config_alertas["mms"]["ativar"]:
        sma = SMAIndicator(close=df["close"], window=config_alertas["mms"]["periodo"])
        resultado["mms"] = sma.sma_indicator().iloc[-1]

    # Volume
    if indicadores_ativos.get("usar_volume") and config_alertas["volume"]["ativar"]:
        volume_ma = df["volume"].rolling(window=config_alertas["volume"]["periodo"]).mean()
        resultado["volume_medio"] = volume_ma.iloc[-1]
        resultado["volume_atual"] = df["volume"].iloc[-1]

    # Estocástico
    if indicadores_ativos.get("usar_estocastico") and config_alertas["estocastico"]["ativar"]:
        stoch = StochasticOscillator(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            window=config_alertas["estocastico"]["k"],
            smooth_window=config_alertas["estocastico"]["d"]
        )
        resultado["estocastico_k"] = stoch.stoch().iloc[-1]
        resultado["estocastico_d"] = stoch.stoch_signal().iloc[-1]

    return resultado
