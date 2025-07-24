import json
import os

# Caminhos relativos aos arquivos
BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DEFAULTS_PATH = os.path.join(BASE_DIR, "config_padrao.json")

def carregar_valores_padrao():
    with open(DEFAULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    moedas = config["geral"]["coin"]
    alertas = config.get("alertas", {})
    valores_padrao = carregar_valores_padrao()
    alterado = False

    for moeda in moedas:
        if moeda not in alertas:
            print(f"🔧 Adicionando configuração padrão para nova moeda: {moeda}")
            alertas[moeda] = valores_padrao
            alterado = True

    if alterado:
        config["alertas"] = alertas
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
            print("✅ config.json atualizado com novas moedas")

    return config
