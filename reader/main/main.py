from config_handler import carregar_config
from fetcher import get_all_candles
from indicators import calcular_indicadores
from processor import analisar_sinais
from database import criar_tabela, salvar_velas
import time

def executar_reader():
    print("🚀 Iniciando Reader...\n")

    # Garante que a tabela está criada
    criar_tabela()

    # Carrega configuração
    config = carregar_config()

    # Coleta os dados de candles
    dados = get_all_candles(config)

    # Loop por moeda
    for moeda in config["geral"]["coin"]:
        candles = dados.get(moeda, [])

        if not candles or len(candles) < 20:
            print(f"⚠️ Dados insuficientes para {moeda}, pulando...\n")
            continue

        # Salva candles no banco
        salvar_velas(moeda, candles)

        # Calcula os indicadores
        indicadores = calcular_indicadores(
            candles,
            config["alertas"][moeda],
            config["indicadores"]
        )

        # Processa sinais
        sinais = analisar_sinais(
            moeda,
            indicadores,
            config["alertas"][moeda]
        )

        # Exibe resultado
        print(f"📊 Alerta para {moeda}:")
        print(sinais)
        print("-" * 40)

if __name__ == "__main__":
    while True:
        executar_reader()
        time.sleep(60)  # Repetição a cada minuto (ajustável)
