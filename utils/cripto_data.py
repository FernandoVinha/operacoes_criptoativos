# utils/cripto_data.py

codigos_operacao = {
    "I": "Compra e venda",
    "II": "Permuta",
    "III": "Doação",
    "IV": "Transferência de criptoativo para a Exchange",
    "V": "Retirada de criptoativo da Exchange",
    "VI": "Cessão temporária (aluguel)",
    "VII": "Dação em pagamento",
    "VIII": "Emissão",
    "IX": "Outras operações que impliquem em transferência de criptoativos"
}

tipos_ni = {
    "1": "CPF",
    "2": "CNPJ",
    "3": "NIF (Número de Identificação Fiscal Pessoa Física)",
    "4": "NIF (Número de Identificação Fiscal Pessoa Jurídica)",
    "5": "Passaporte",
    "6": "O país da PF ou PJ não possui NIF",
    "7": "O país da PF ou PJ POSSUI NIF mas a pessoa não possui"
}

tipos_registro = {
    "0000": "Abertura do arquivo digital e identificação da Exchange",
    "0110": "Registra as operações de compra e venda",
    "0210": "Registra as operações de permuta",
    "0410": "Registra as operações de transferência de criptoativos para a Exchange",
    "0510": "Registra as operações de retirada de criptoativos da Exchange",
    "0710": "Registra as operações de dação em pagamento",
    "0910": "Registra outras operações de transferência de criptoativos",
    "1000": "Registra os saldos anuais de moedas fiduciárias e criptoativos nas contas dos clientes da Exchange",
    "1010": "Registra os saldos anuais de criptoativos",
    "9999": "Encerramento do arquivo digital"
}
