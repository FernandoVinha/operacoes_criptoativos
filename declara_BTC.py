import os
from datetime import datetime
from extract_pdf_data import extract_data_from_pdf

def format_output_0110(data):
    return {
        "TIPO DE REGISTRO": "0110",
        "OperacaoData": data["Data de Emissão"].replace("/", ""),
        "OperacaoCodigo": "I",
        "OperacaoValor": data["Valor Total"].replace(",", "").replace(".", ""),
        "CriptoativoSimbolo": "BTC",
        "CriptoativoQuantidade": data["Qtde"].replace(",", "").replace(".", ""),
        "CompradorExchangeNome": data["Exchange"],
        "CompradorExchangeURL": data["ExchangeURL"],
        "CompradorExchangePais": "BR"
    }

def format_output_9999(data):
    return {
        "TIPO DE REGISTRO": "9999"
    }

def save_output_to_file(outputs, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for output in outputs:
            output_line = "|".join(output.values()) + "\r\n"
            file.write(output_line.rstrip('|'))

def generate_client_file(data, output_file_path):
    outputs = []

    if "0110" in data:
        outputs.extend(data["0110"])

    outputs.append(format_output_9999(data))

    save_output_to_file(outputs, output_file_path)

# Exemplo de uso
if __name__ == "__main__":
    pdf_path = "caminho/para/o/seu/arquivo.pdf"
    data = extract_data_from_pdf(pdf_path)

    # Simular dados de exemplo
    data["ExchangeURL"] = "https://www.exemplo.com"
    data["0110"] = [
        {"TIPO DE REGISTRO": "0110", "OperacaoData": "01012020", "OperacaoID": "1", "OperacaoCodigo": "I", "OperacaoValor": "100.00",
         "OperacaoTaxasValor": "1.00", "CriptoativoSimbolo": "BTC", "CriptoativoQuantidade": "0.1", "CompradorExchangeNome": "Nome da Exchange"}
    ]

    output_file_path = "registro_client.txt"
    generate_client_file(data, output_file_path)
