from datetime import datetime

def analisar_sinais(moeda, indicadores, alertas_config):
    sinais = {}

    # RSI
    if "rsi" in indicadores and alertas_config["rsi"]["ativar"]:
        rsi_valor = indicadores["rsi"]
        sinais["rsi_compra"] = rsi_valor < alertas_config["rsi"]["compra_limite"]
        sinais["rsi_venda"] = rsi_valor > alertas_config["rsi"]["venda_limite"]

    # MACD
    if "macd_line" in indicadores and alertas_config["macd"]["ativar"]:
        macd_line = indicadores["macd_line"]
        macd_signal = indicadores["macd_signal"]
        sinais["macd_crossover_alta"] = macd_line > macd_signal
        sinais["macd_crossover_baixa"] = macd_line < macd_signal

    # MMS (média móvel simples)
    if "mms" in indicadores and alertas_config["mms"]["ativar"]:
        preco_atual = indicadores.get("close") or indicadores.get("preco")  # adaptável
        media = indicadores["mms"]
        sinais["mms_cruzou_para_cima"] = preco_atual > media
        sinais["mms_cruzou_para_baixo"] = preco_atual < media

    # Volume
    if "volume_atual" in indicadores and alertas_config["volume"]["ativar"]:
        sinais["volume_acima_media"] = indicadores["volume_atual"] > indicadores["volume_medio"]
        sinais["volume_abaixo_media"] = indicadores["volume_atual"] < indicadores["volume_medio"]

    # Estocástico
    if "estocastico_k" in indicadores and alertas_config["estocastico"]["ativar"]:
        k = indicadores["estocastico_k"]
        sinais["estocastico_sobrevendido"] = k < 20
        sinais["estocastico_sobrecomprado"] = k > 80

    # Decisões finais
    alerta_compra = (
        sinais.get("rsi_compra") or
        sinais.get("macd_crossover_alta") or
        sinais.get("mms_cruzou_para_cima") or
        sinais.get("volume_acima_media") or
        sinais.get("estocastico_sobrevendido")
    )

    alerta_venda = (
        sinais.get("rsi_venda") or
        sinais.get("macd_crossover_baixa") or
        sinais.get("mms_cruzou_para_baixo") or
        sinais.get("volume_abaixo_media") or
        sinais.get("estocastico_sobrecomprado")
    )

    return {
        "moeda": moeda,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sinais_ativos": sinais,
        "alerta_compra": bool(alerta_compra),
        "alerta_venda": bool(alerta_venda)
    }
