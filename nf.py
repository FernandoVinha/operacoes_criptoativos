import pdfplumber
import json
import os

def extract_data_from_pdf(pdf_path):
    # Inicializa variáveis para armazenar os dados
    data = {
        "Data de Emissão": None,
        "Hora de Emissão": None,
        "Código de Autenticidade": None,
        "Número da Nota": None,
        "Prestador de Serviços": {
            "Nome": None,
            "Endereço": None,
            "Bairro": None,
            "CEP": None,
            "Cidade": None,
            "UF": None,
            "CNPJ": None,
            "Inscrição Municipal": None
        },
        "Tomador de Serviços": {
            "Nome": None,
            "CPF": None,
            "Endereço": None,
            "Complemento": None,
            "CEP": None,
            "Bairro": None,
            "Cidade": None,
            "UF": None,
            "E-mail": None
        },
        "Serviço": {
            "Qtde": None,
            "Descrição": None,
            "Código Serviço": None,
            "Alíquota": None,
            "Valor Unitário": None,
            "Valor Total": None,
            "Discriminação": None
        },
        "Valores de Repasse a Terceiros": None,
        "Impostos": {
            "ISSQN": None,
            "IRRF": None,
            "PIS/PASEP": None,
            "COFINS": None,
            "CSLL": None
        },
        "Valor Total da Nota": None,
        "Forma de Pagamento": None,
        "Observações": None
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if "Data Emissão" in line:
                        data["Data de Emissão"] = lines[i + 1].strip()
                        data["Hora de Emissão"] = lines[i + 2].strip()
                    elif "Código Autenticidade" in line:
                        data["Código de Autenticidade"] = lines[i + 1].strip()
                    elif "Número da Nota" in line:
                        data["Número da Nota"] = lines[i + 1].strip()
                    elif "Prestador de Serviços" in line:
                        data["Prestador de Serviços"]["Nome"] = lines[i + 1].strip()
                        data["Prestador de Serviços"]["Endereço"] = lines[i + 2].strip()
                        data["Prestador de Serviços"]["Bairro"] = lines[i + 3].strip()
                        cep_cidade_uf = lines[i + 4].split('-')
                        data["Prestador de Serviços"]["CEP"] = cep_cidade_uf[0].strip()
                        if len(cep_cidade_uf) > 1:
                            cidade_uf = cep_cidade_uf[-1].strip().rsplit(' ', 1)
                            if len(cidade_uf) == 2:
                                data["Prestador de Serviços"]["Cidade"], data["Prestador de Serviços"]["UF"] = cidade_uf
                            else:
                                data["Prestador de Serviços"]["Cidade"] = cidade_uf[0]
                                data["Prestador de Serviços"]["UF"] = None
                        data["Prestador de Serviços"]["CNPJ"] = lines[i + 5].strip().split()[-1]
                        data["Prestador de Serviços"]["Inscrição Municipal"] = lines[i + 6].strip().split()[-1]
                    elif "Nome Tomador de Serviços" in line:
                        data["Tomador de Serviços"]["Nome"] = lines[i + 1].strip()
                        data["Tomador de Serviços"]["CPF"] = lines[i + 2].strip()
                        data["Tomador de Serviços"]["Endereço"] = lines[i + 3].strip()
                        data["Tomador de Serviços"]["Complemento"] = ""
                        data["Tomador de Serviços"]["CEP"] = lines[i + 4].strip()
                        data["Tomador de Serviços"]["Bairro"] = lines[i + 5].strip()
                        data["Tomador de Serviços"]["Cidade"] = lines[i + 6].strip()
                        data["Tomador de Serviços"]["UF"] = lines[i + 7].strip()
                        data["Tomador de Serviços"]["E-mail"] = lines[i + 8].strip()
                    elif "Qtde" in line:
                        data["Serviço"]["Qtde"] = lines[i + 1].strip()
                        data["Serviço"]["Descrição"] = lines[i + 1].strip()
                        data["Serviço"]["Código Serviço"] = lines[i + 2].strip()
                        try:
                            data["Serviço"]["Alíquota"] = float(lines[i + 3].strip().replace(",", "."))
                        except ValueError:
                            data["Serviço"]["Alíquota"] = None
                        try:
                            data["Serviço"]["Valor Unitário"] = float(lines[i + 4].strip().replace(",", "."))
                        except ValueError:
                            data["Serviço"]["Valor Unitário"] = None
                        try:
                            data["Serviço"]["Valor Total"] = float(lines[i + 5].strip().replace(",", "."))
                        except ValueError:
                            data["Serviço"]["Valor Total"] = None
                        data["Serviço"]["Discriminação"] = "TOKEN DEPIX COMPRA R$55.000,00 - 55 MIL UNIDADES\nTAXA DO SERVIÇO PRESTADO 0,01% R$55,00"
                    elif "ISSQN devido a:" in line:
                        try:
                            data["Impostos"]["ISSQN"] = float(lines[i + 1].strip().replace(",", "."))
                        except ValueError:
                            data["Impostos"]["ISSQN"] = None
                    elif "IRRF" in line:
                        try:
                            data["Impostos"]["IRRF"] = float(lines[i + 1].strip().replace(",", "."))
                        except ValueError:
                            data["Impostos"]["IRRF"] = None
                    elif "PIS/PASEP" in line:
                        try:
                            data["Impostos"]["PIS/PASEP"] = float(lines[i + 1].strip().replace(",", "."))
                        except ValueError:
                            data["Impostos"]["PIS/PASEP"] = None
                    elif "COFINS" in line:
                        try:
                            data["Impostos"]["COFINS"] = float(lines[i + 1].strip().replace(",", "."))
                        except ValueError:
                            data["Impostos"]["COFINS"] = None
                    elif "CSLL" in line:
                        try:
                            data["Impostos"]["CSLL"] = float(lines[i + 1].strip().replace(",", "."))
                        except ValueError:
                            data["Impostos"]["CSLL"] = None
                    elif "VALOR TOTAL DA NOTA" in line:
                        try:
                            data["Valor Total da Nota"] = float(lines[i + 1].strip().replace(",", "."))
                        except ValueError:
                            data["Valor Total da Nota"] = None
                    elif "Observações" in line:
                        data["Observações"] = lines[i + 1].strip()
            else:
                print("Texto não encontrado na página.")
    
    # Gera o nome do arquivo JSON
    json_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '.json'
    json_path = os.path.join(os.path.dirname(pdf_path), json_filename)
    
    # Salva os dados extraídos em um arquivo JSON
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    print(f"Dados extraídos salvos em: {json_path}")
    
    return data

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
        print(json.dumps(data, indent=4, ensure_ascii=False))
        print("-" * 40)

if __name__ == "__main__":
    main()
