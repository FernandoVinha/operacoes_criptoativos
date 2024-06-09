import os
import json
from nf import extract_data_from_pdf

def find_pdfs_in_directory(directory):
    # Lista todos os arquivos no diretório especificado
    files = os.listdir(directory)
    
    # Filtra apenas os arquivos com extensão .pdf
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    
    return pdf_files

def load_json_data(json_path):
    # Carrega os dados do arquivo JSON
    with open(json_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def main():
    # Obtém o diretório onde o código está sendo executado
    directory = os.getcwd()

    # Encontra todos os arquivos PDF no diretório
    pdf_files = find_pdfs_in_directory(directory)
    
    # Verifica se encontrou algum PDF
    if not pdf_files:
        print("Nenhum arquivo PDF encontrado na pasta.")
        return
    
    # Processa cada PDF encontrado
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        print(f"Processando o arquivo: {pdf_path}")
        
        # Chama a função para extrair os dados do PDF e gerar o JSON
        extract_data_from_pdf(pdf_path)
        
        # Gera o caminho do arquivo JSON correspondente
        json_filename = os.path.splitext(pdf_file)[0] + '.json'
        json_path = os.path.join(directory, json_filename)
        
        # Carrega e imprime os dados do JSON
        data = load_json_data(json_path)
        print(f"Dados extraídos do JSON {json_filename}:")
        for key, value in data.items():
            print(f"{key}: {value}")
        print("-" * 40)

if __name__ == "__main__":
    main()
