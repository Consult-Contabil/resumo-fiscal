import pdfplumber
import re
from flask import Flask, render_template, request
from tabulate import tabulate
import locale
import os
import emoji
from collections import defaultdict
from babel.numbers import format_currency


app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

def converter_pdf_para_texto(caminho_arquivo_pdf):
    texto = ""
    with pdfplumber.open(caminho_arquivo_pdf) as pdf:
        for page in pdf.pages:
            texto += page.extract_text()

    padrao_cnpj = r"CNPJ:\s+(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})"
    resultado_cnpj = re.search(padrao_cnpj, texto)
    cnpj = resultado_cnpj.group(1) if resultado_cnpj else ""

    padrao_nome_empresa = r"CNPJ:\s+[\d\s.-]+-\s+(.*)"
    resultado_nome_empresa = re.search(padrao_nome_empresa, texto)
    nome_empresa = resultado_nome_empresa.group(1) if resultado_nome_empresa else ""
    # print(texto)
    return texto, nome_empresa, cnpj

def buscar_valores_debitos(texto_pdf):
    resultados = {}

    # padrao_linha1 = r"([A-Za-z.-]+)\s+\d{2}/\d{4}\s+\d{2}/\d{2}/\d{4}\s+[\d.,]+\s+([\d.,]+)\s+[\d.,]+\s+[\d.,]+\s+[\d.,]+\s+DEVEDOR"
    padrao_linha1 = r"([A-Za-z.-]+)\s+\d{2}/?\d{4}\s+\d{2}/\d{2}/\d{4}\s+[\d.,]+\s+([\d.,]+)\s+[\d.,]+\s+[\d.,]+\s+[\d.,]+\s+DEVEDOR"
    padrao_linha2 = r"(SIMPLES NAC\.)\s+\d{2}/\d{4}(?:\s+\d{2}/\d{2}/\d{4})?\s+[\d.,]+\s+([\d.,]+)\s+DEVEDOR"
    padrao_linha3 = r"(\d{4}-\d{2} - [A-Za-z.-]+)\s+\d{4}\s+\d{2}/\d{2}/\d{4}\s+[\d.,]+\s+([\d.,]+)\s+DEVEDOR"
    padrao_linha4 = r"\d{4}-\d{2} - ([\w\s/º.-]+)\s+\d{2}/\d{2}/\d{4}\s+\d{2}/\d{2}/\d{4}\s+([\d.,]+)\s+([\d.,]+)\s+DEVEDOR"
    padrao_linha5 = r"\d{4}-\d{2} - ([A-Za-z]+)\s+\d{1,2}º\s+\d{2}/\d{2}/\d{4}\s+[\d.,]+\s+([\d.,]+)\s+[\d.,]+\s+[\d.,]+\s+[\d.,]+\s+DEVEDOR"
    padrao_linha6 = r"\d{4}-\d{2} - ([A-Za-z\s-]+)\s+\d{2}/\d{2}/\d{4}\s+\d{2}/\d{2}/\d{4}\s+[\d.,]+\s+([\d.,]+)\s+[\d.,]+\s+[\d.,]+\s+[\d.,]+\s+DEVEDOR"
    padrao_linha7 = r"([A-Za-z.-]+)\s+\d{4}\s+\d{2}/\d{2}/\d{4}\s+[\d.,]+\s+([\d.,]+)\s+[\d.,]+\s+[\d.,]+\s+[\d.,]+\s+DEVEDOR"
    padrao_linha8 = r"\d{4}-\d{2} - ([A-Za-z\s-]+)\s+\d{4}\s+\d{2}/\d{2}/\d{4}\s+[\d.,]+\s+([\d.,]+)\s+[\d.,]+\s+[\d.,]+\s+[\d.,]+\s+DEVEDOR"



    matches1 = re.findall(padrao_linha1, texto_pdf, flags=re.IGNORECASE)
    matches2 = re.findall(padrao_linha2, texto_pdf, flags=re.IGNORECASE)
    matches3 = re.findall(padrao_linha3, texto_pdf, flags=re.IGNORECASE)
    matches4 = re.findall(padrao_linha4, texto_pdf, flags=re.IGNORECASE)
    matches5 = re.findall(padrao_linha5, texto_pdf, flags=re.IGNORECASE)
    matches6 = re.findall(padrao_linha6, texto_pdf, flags=re.IGNORECASE)
    matches7 = re.findall(padrao_linha7, texto_pdf, flags=re.IGNORECASE)
    matches8 = re.findall(padrao_linha8, texto_pdf, flags=re.IGNORECASE)

    for match in matches1:
        nome_debito = match[0].strip()
        saldo_devedor = float(match[1].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor

    for match in matches2:
        nome_debito = match[0].strip()
        saldo_devedor = float(match[1].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor

    for match in matches3:
        nome_debito = match[0].split(" - ", 1)[1].strip()
        saldo_devedor = float(match[1].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor

    for match in matches4:
        nome_debito = match[0].split(" - ", 0)[-1].strip()
        saldo_devedor = float(match[1].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor

    for match in matches5:
        nome_debito = match[0].strip()
        trimestre = match[0].split(" ")
        saldo_devedor = float(match[1].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor
    
    for match in matches6:
        nome_debito = match[0].strip()
        saldo_devedor = float(match[1].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor

    for match in matches7:
        nome_debito = match[0].strip()
        saldo_devedor = float(match[1].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor

    for match in matches8:
        nome_debito = match[0].strip()
        saldo_devedor = float(match[1].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor

    resultados = {nome: round(valor, 2) for nome, valor in resultados.items()}
    print("Resultados")
    print(resultados)
    return resultados    

def extrair_debitos_exigibilidade_suspensa(texto_pdf):
    resultados = {}
    padrao1 = r"(\d{4}-\d{2}) - (PGDAS-D) - (MULTA) (\d{2}/\d{2}/\d{4}) (\d{2}/\d{2}/\d{4}) ([\d,.]+) ([\d,.]+) (A VENCER)"
    padrao2 = r"(\d{4}-\d{2}) - (CP-SEGUR.) (\d{2}/\d{4}) (\d{2}/\d{2}/\d{4}) ([\d,.]+) ([\d,.]+) (A ANALISAR)"
    padrao3 = r"(\d{4}-\d{2}) - (CP-PATRONAL) (\d{2}/\d{4}) (\d{2}/\d{2}/\d{4}) ([\d,.]+) ([\d,.]+) (A ANALISAR)"
    padrao4 = r"(\d{4}-\d{2}) - (CP-TERCEIROS) (\d{2}/\d{4}) (\d{2}/\d{2}/\d{4}) ([\d,.]+) ([\d,.]+) (A ANALISAR)"
    padrao5 = r"(\d{4}-\d{2}) - (DCTF) - (MULTA ATR) (\d{2}/\d{2}/\d{4}) (\d{2}/\d{2}/\d{4}) ([\d,.]+) ([\d,.]+) (A VENCER)"
    
    matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
    matches2 = re.findall(padrao2, texto_pdf, re.DOTALL)
    matches3 = re.findall(padrao3, texto_pdf, re.DOTALL)
    matches4 = re.findall(padrao4, texto_pdf, re.DOTALL)
    matches5 = re.findall(padrao5, texto_pdf, re.DOTALL)
    
    for match in matches1:
        nome_debito = match[1]
        saldo_devedor = float(match[6].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor
    
    for match in matches2:
        nome_debito = match[1]
        saldo_devedor = float(match[5].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor
    
    for match in matches3:
        nome_debito = match[1]
        saldo_devedor = float(match[5].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor

    for match in matches4:
        nome_debito = match[1]
        saldo_devedor = float(match[5].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor
    
    for match in matches5:
        nome_debito = match[1]
        saldo_devedor = float(match[5].replace(".", "").replace(",", "."))

        if nome_debito in resultados:
            resultados[nome_debito] += saldo_devedor
        else:
            resultados[nome_debito] = saldo_devedor

    resultados = {nome: round(valor, 2) for nome, valor in resultados.items()}

    return resultados

def pendencia_parcelamento_sipade(texto_pdf): #Pendência - Parcelamento SIPADE
    padrao2 = r"(\d{5}\.\d{3}\.\d{3}/\d{4}-\d{2}) (\d{4}-[A-Z]+)"

    matches2 = re.findall(padrao2, texto_pdf, re.DOTALL)
    processos = 0
    processos_li = []

    for match in matches2:
        processos_li.append(match[0])
        processos += 1
        # print(f'padrão 02: {match[1]}')
    
    processos_formatados = '\n'.join(processos_li)
    # print(f' pendencia parcelamento sipade: {processos_formatados}')

    return processos, processos_formatados

def pendencia_divergencia(texto_pdf):
    resultados = {}
    padrao1 = r"(\d{2}/\d{4})\s+(\d+)\s+([A-Za-z\s]+)\s+([\d.,]+)"
    padrao2 = r"(\d{2}/\d{4}) (\d{3}) (.*?) ([\d.,]+)"
    padrao3 = r"(\d{3})\s+([A-Za-z]+)\s+([A-Za-z\s]+)\s+([\d.,]+)"

    matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
    matches2 = re.findall(padrao2, texto_pdf, re.DOTALL)
    matches3 = re.findall(padrao3, texto_pdf, re.DOTALL)
    
    for match in matches1:
        codigo = match[1]
        nome_debito = match[2].split(' ', 1)[0]
        tipo_debito = match[2].split(' ', 1)[1]
        saldo_devedor = float(match[3].replace(".", "").replace(",", "."))

        chave = f"{codigo} {nome_debito} {tipo_debito}"
        if chave in resultados:
            resultados[chave]["Valores"].append(saldo_devedor)
            resultados[chave]["Total"] += saldo_devedor
        else:
            resultados[chave] = {"Valores": [saldo_devedor], "Total": saldo_devedor}
    
    for match in matches2:
        codigo = match[1]
        nome_debito = match[2].split(' ', 1)[0]
        tipo_debito = match[2].split(' ', 1)[1]
        saldo_devedor = float(match[3].replace(".", "").replace(",", "."))
        chave = f"{codigo} {nome_debito} {tipo_debito}"
        if chave in resultados:
            resultados[chave]["Valores"].append(saldo_devedor)
            resultados[chave]["Total"] += saldo_devedor
        else:
            resultados[chave] = {"Valores": [], "Total": 0}
            resultados[chave]["Valores"].append(saldo_devedor)
            resultados[chave]["Total"] = saldo_devedor
    
    for match in matches3:
        codigo = match[0]
        nome_debito = match[1]
        tipo_debito = match[2].strip()
        saldo_devedor = float(match[3].replace(".", "").replace(",", "."))
        chave = f"{codigo} {nome_debito} {tipo_debito}"
        if chave in resultados:
            resultados[chave]["Valores"].append(saldo_devedor)
            resultados[chave]["Total"] += saldo_devedor
        else:
            resultados[chave] = {"Valores": [], "Total": 0}
            resultados[chave]["Valores"].append(saldo_devedor)
            resultados[chave]["Total"] = saldo_devedor
    
    total_geral = sum([dados["Total"] for chave, dados in resultados.items()])
    tabela_resultados = []
    for chave, dados in resultados.items():
        codigo, nome_debito = chave.split(' ', 1)
        total = format_currency(dados["Total"], "BRL", locale="pt_BR")
        tabela_resultados.append([codigo, nome_debito, total])

    resultado_table = tabulate(tabela_resultados, headers=["Código do débito", "Nome do débito", "Total"], tablefmt="html")

    return resultado_table, total_geral

def pendencia_omissao_gfip(texto_pdf): #Pendência - Omissão de GFIP
    padrao1 = r"\(Período de Apuração\) CNPJ/CEI:\s([\d\./-]+)\s(\d+)\s-\s([A-Z\s0-9º]+)\n"
    matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
    processos_li = []

    num_pendencias = 0  # Variável para contar a quantidade de pendências
    # print(matches1)

    for match in matches1:
        processos_li.append(match[1])
        processos_li.append(match[2])
        num_pendencias += 1  # Incrementa a variável ao encontrar uma pendência
        # print(f'gfip: {match}')
    
    processos_formatados = '\n'.join(processos_li)
    # print(processos_formatados)

    return processos_formatados, num_pendencias

def pendencia_omissao_dctfweb(texto_pdf): #Pendência - Omissão de DCTFWeb
    padrao1 = r"(\d{4}) - ((?:JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)(?:\s(?:JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ))*)"
    matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
    processos_li = []

    num_pendencias = 0  # Variável para contar a quantidade de pendências
    # print(matches1)
    for match in matches1:
        processos_li.append(match[0])
        for month in match[1:]:
            processos_li.append(month)
            num_pendencias += 1  # Incrementa a variável ao encontrar uma pendência
        # print(f'dctfweb: {match}')
    
    processos_formatados = '\n'.join(processos_li)
    # print(processos_formatados)

    return processos_formatados, num_pendencias

def pendencia_omissao_dctf(texto_pdf): #Pendência - Omissão de DCTF
    padrao1 = r"(\d{4}) - ((?:JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)(?:\s(?:JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ))*)"
    ini_point = r"Omissão de DCTF"
    end_point = r"Omissão de EFD-CONTRIB"
    ini_match = re.search(ini_point, texto_pdf, re.DOTALL)
    end_match = re.search(end_point, texto_pdf, re.DOTALL)
    processos_li = []
    num_pendencias = 0  # Variável para contar a quantidade de pendências

    if ini_match and end_match:
        ini_pos = ini_match.end()
        end_pos = end_match.start()
        texto_pdf_subset = texto_pdf[ini_pos:end_pos]
        matches1 = re.findall(padrao1, texto_pdf_subset, re.DOTALL)
        for match in matches1:
            processos_li.append(match[0])
            for month in match[1:]:
                processos_li.append(month)
                num_pendencias += 1  # Incrementa a variável ao encontrar uma pendência
            # print(f'dctf: {match}')
    else:
        matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
        for match in matches1:
            processos_li.append(match[0])
            for month in match[1:]:
                processos_li.append(month)
                num_pendencias += 1  # Incrementa a variável ao encontrar uma pendência
            # print(f'dctf: {match}')
    
    processos_formatados = '\n'.join(processos_li)
    # print(processos_formatados)

    return processos_formatados, num_pendencias

def pendencia_efd(texto_pdf): #Pendência - Omissão de EFD
    padrao1 = r"(\d{4}) - ((?:JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)(?:\s(?:JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ))*)"
    ini_point = r"Omissão de EFD-CONTRIB"
    ini_match = re.search(ini_point, texto_pdf, re.DOTALL)
    if ini_match:
        ini_pos = ini_match.end()
        texto_pdf_subset = texto_pdf[ini_pos:]
        matches1 = re.findall(padrao1, texto_pdf_subset, re.DOTALL)
        processos_li = []
        num_pendencias = 0  # Variável para contar a quantidade de pendências
        # print(matches1)
        for match in matches1:
            processos_li.append(match[0])
            for month in match[1:]:
                processos_li.append(month)
                num_pendencias += 1  # Incrementa a variável ao encontrar uma pendência
            # print(f'dctf: {match}')
    else:
        matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
        num_pendencias = 0 
        processos_li = []
        # print('teste func')
        # print(matches1)
        for match in matches1:
            processos_li.append(match[0])
            for month in match[1:]:
                processos_li.append(month)
                num_pendencias += 1  # Incrementa a variável ao encontrar uma pendência
            # print(f'dctf: {match}')
    processos_formatados = '\n'.join(processos_li)
    # print(processos_formatados)

    return processos_formatados, num_pendencias

def pendencia_ecf(texto_pdf): #Pendência - Omissão de ECF
    padrao1 = r"\(Ano-Calendário\) (\d{4})"
    matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
    processos_li = []
    num_pendencias = 0  # Variável para contar a quantidade de pendências
    # print(matches1)
    for match in matches1:
        processos_li.append(match)
        num_pendencias += 1  # Incrementa a variável ao encontrar uma pendência
        # print(f'dctfweb: {match}')
    
    processos_formatados = '\n'.join(processos_li)
    # print(processos_formatados)

    return processos_formatados, num_pendencias

def somar_pendencias(texto_pdf):

    total_pendencias = 0

    _, num_pendencias_gfip = pendencia_omissao_gfip(texto_pdf)
    total_pendencias += num_pendencias_gfip

    _, num_pendencias_dctfweb = pendencia_omissao_dctfweb(texto_pdf)
    total_pendencias += num_pendencias_dctfweb

    _, num_pendencias_dctf = pendencia_omissao_dctf(texto_pdf)
    total_pendencias += num_pendencias_dctf

    _, num_pendencias_efd = pendencia_efd(texto_pdf)
    total_pendencias += num_pendencias_efd

    _, num_pendencias_ecf = pendencia_ecf(texto_pdf)
    total_pendencias += num_pendencias_ecf

    return total_pendencias

def pednencia_debito_sicob(texto_pdf): #Pendência - Débito (SICOB)
    padrao1 = r"Débito:\s(\d+-\d)\sSituação:\s(\d+\s-\s[A-Z\.]+)"

    matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
    processos = 0
    processos_li = []

    for match in matches1:
        processos_li.append(match[0])
        processos += 1
    
    processos_formatados = '\n'.join(processos_li)
    # print(processos_formatados)
    # print(processos)

    return processos, processos_formatados

def count_pendencia_processo_fiscal(texto_pdf): #Pendência - Processo Fiscal (SIEF)
    padrao1 =  r"(\d{3}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (DEVEDOR [A-Z\s-]+ [A-Z\s-]+)"  
    matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
    processos = 0
    processos_li = []
    for match in matches1:
        processos_li.append(match[0])
        processos += 1
    
    processos_formatados = '\n'.join(processos_li)
    # print(processos_formatados)

    return processos, processos_formatados

def count_pendencia_processo_fiscal_exg(texto_pdf): #Processo Fiscal com Exigibilidade Suspensa (SIEF)
    padrao1 = r"(\d{2}\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (SUSPENSO-MEDIDA JUDICIAL Val\. Analise: \d{2}/\d{2}/\d{4} DEL REC FED ADMINIST TRIBUTARIA-FOR-CE)"
    padrao2 = r"(\d{2}\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (DEVEDOR-EM JULGAMENTO DA MANIFESTACAO INCONFORMIDADE \(CREDITO\) SEC ORIENT ANALISE TRIBUTARIA-DRF-TSA-PI)"
    padrao3 = r"(\d{2}\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (SUSPENSO-JULGAMENTO DO RECURSO VOLUNTARIO CONSELHO ADMINIST RECURSOS FISCAIS-MF-DF)"
    matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
    matches2 = re.findall(padrao2, texto_pdf, re.DOTALL)
    matches3 = re.findall(padrao3, texto_pdf, re.DOTALL)
    processos = 0

    for match in matches1:
        processos += 1
    for match in matches2:
        processos += 1
    for match in matches3:
        processos += 1
    
    return processos

def count_pendencia_parcelamento_siefpar(texto_pdf): # Pendência – Parcelamento (SIEFPAR)
    padrao1 = r"Parcelamento: (\d+) Parcelas em Atraso: (\d+) Valor em Atraso: ([\d,.]+)"
    padrao2 = r"Parcelamento: (\d+) Valor Suspenso: ([\d,.]+)"
    matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
    matches2 = re.findall(padrao2, texto_pdf, re.DOTALL)
    saldo_devedor = 0
    for match in matches1:
        saldo_devedor = float(match[2].replace(".", "").replace(",", "."))
    for match in matches2:
        saldo_devedor = float(match[1].replace(".", "").replace(",", "."))
    
    return saldo_devedor

def count_pendencia_insc_sida(texto_pdf): #Pendência - Inscrição (SIDA)
    padrao10 = r"(\d{2}\.\d{1,2}\.\d{2}\.\d{6}-\d{2}) (\d{4}-) (\d{2}\/\d{2}\/\d{4}) (\d{3,}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (DEVEDOR PRINCIPAL)\n([A-Z\s]+)"
    padrao13 = r"(\d{2}\.\d{1,2}\.\d{2}\.\d{6}-\d{2}) (\d{4}-[A-Z]+) (\d{2}/\d{2}/\d{4}) (\d{2}/\d{2}/\d{4}) (\d{3,}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (DEVEDOR PRINCIPAL)\n([A-Z\s]+)"
    padrao15 = r"(\d{2}\.\d{1,2}\.\d{2}\.\d{6}-\d{2}) (\d{4}-[A-Z]+) (\d{2}\/\d{2}\/\d{4}) (\d{3,}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (DEVEDOR\sPRINCIPALMINISTÉRIO)"
    padrao14 = r"(\d{2}\.\d{1,2}\.\d{2}\.\d{6}-\d{2}) (\d{4}-[A-Z\.]+) (\d{2}\/\d{2}\/\d{4}) (\d{3,}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (DEVEDOR PRINCIPAL)\n([A-Z\.]+)"
    end_point = r"Inscrição com Exigibilidade Suspensa \(SIDA\)"
    ini_point = r"Pendência - Inscrição \(SIDA\)"

    ini_match = re.search(ini_point, texto_pdf, re.DOTALL)
    end_match = re.search(end_point, texto_pdf, re.DOTALL)
    pendencias = 0
    # print(end_match)
    # print(ini_match)
    processos = []
    if end_match:
        if ini_match and end_match:
            ini_pos = ini_match.end()
            end_pos = end_match.start()

            texto_pdf_subset = texto_pdf[ini_pos:end_pos]
            matches10 = re.findall(padrao10, texto_pdf_subset, re.DOTALL)
            matches13 = re.findall(padrao13, texto_pdf_subset, re.DOTALL)
            matches14 = re.findall(padrao14, texto_pdf_subset, re.DOTALL)
            matches15 = re.findall(padrao15, texto_pdf_subset, re.DOTALL)
            

            for match in matches10:
                # print(match[0])
                processos.append(match[0])
                pendencias += 1
                # print(match)
                # print("controle-5")
            for match in matches13:
                # print(match[0])
                pendencias += 1
                processos.append(match[0])
                # print(match)
                # print("controle-8")
            
            for match in matches14:
                # print(match[0])
                pendencias += 1
                processos.append(match[0])
                # print(match)
                # print("controle-9")
            for match in matches15:
                # print('iniciando o match 15')
                # print(match[0])
                pendencias += 1
                processos.append(match[0])
                # print(match)
                # print("controle-10")

        
    elif ini_match:
        matches10 = re.findall(padrao10, texto_pdf, re.DOTALL)
        matches13 = re.findall(padrao13, texto_pdf, re.DOTALL)
        matches14 = re.findall(padrao14, texto_pdf, re.DOTALL)
        
        for match in matches10:
            # print(match[0])
            processos.append(match[0])
            pendencias += 1
            # print(match)
            
        for match in matches13:
            # print(match[0])
            pendencias += 1
            processos.append(match[0])
            # print(match)
        for match in matches14:
            # print(match[0])
            pendencias += 1
            processos.append(match[0])
            # print(match)

    processos_formatados = '\n'.join(processos)
    # print(processos_formatados)
    return pendencias, processos_formatados

def extrair_data(texto_pdf):
    padrao_data = r"PROCURADORIA-GERAL DA FAZENDA NACIONAL (\d{2}/\d{2}/\d{4})"
    match_data = re.search(padrao_data, texto_pdf)
    
    if match_data:
        data = match_data.group(1)  # Obtendo o valor capturado pelo grupo 1
        return data
    else:
        return None  # Retornando None se não encontrar a data

def count_inscricao_exibil_sus_sida(texto_pdf): #Inscrição com Exigibilidade Suspensa (SIDA)
    
    padrao12 = r"(\d{2}\.\d{1,2}\.\d{2}\.\d{6}-\d{2}) (\d{4}-[A-Z\.]+) (\d{2}\/\d{2}\/\d{4}) (\d{3,}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (DEVEDOR PRINCIPAL)"
    padrao13 = r"(\d{2}\.\d{1}\.\d{2}\.\d{6}-\d{2}) (\d{4}-[A-Z\.]+) (\d{2}/\d{2}/\d{4}) (\d{2}/\d{2}/\d{4}) (\d{5}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (DEVEDOR PRINCIPAL)"
    padrao14 = r"(\d{2}\.\d{1}\.\d{2}\.\d{6}-\d{2}) (\d{4}--) (\w+) (\d{2}/\d{2}/\d{4}) (\d{5}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (DEVEDOR PRINCIPAL)\n([A-Z]+)"
    padrao15 = r"(\d{2}\.\d{1}\.\d{2}\.\d{6}-\d{2}) (\d{4}-) (\d{2}/\d{2}/\d{4}) (\d{5}\.\d{3}\.\d{3}\/\d{4}-\d{2}) (DEVEDOR PRINCIPAL)\n([A-Z\.]+)" 
    
    ini_point = r"Inscrição com Exigibilidade Suspensa \(SIDA\)"
    end_point = r"Parcelamento com Exigibilidade Suspensa \(SISPAR\)"

    ini_match = re.search(ini_point, texto_pdf, re.DOTALL)
    end_match = re.search(end_point, texto_pdf, re.DOTALL)
    # print(end_match)
    pendencias = 0
    if end_match:
        if ini_match and end_match:
            ini_pos = ini_match.end()
            end_pos = end_match.start()

            texto_pdf_subset = texto_pdf[ini_pos:end_pos]
            
            matches12 = re.findall(padrao12,  texto_pdf_subset, re.DOTALL)
            matches13 = re.findall(padrao13,  texto_pdf_subset, re.DOTALL)
            matches14 = re.findall(padrao14,  texto_pdf_subset, re.DOTALL)
            matches15 = re.findall(padrao15,  texto_pdf_subset, re.DOTALL)

            for match in matches12:
                # print("controle match 12")
                # print(match)
                pendencias += 1
            for match in matches13:
                # print("controle match 13")
                # print(match)
                pendencias += 1
            for match in matches14:
                # print("controle match 14")
                # print(match)
                pendencias += 1
            for match in matches15:
                # print("controle match 15")
                # print(match)
                pendencias += 1
    elif ini_match:
        ini_pos = ini_match.end()
        texto_pdf_subset = texto_pdf[ini_pos:]

        matches12 = re.findall(padrao12,  texto_pdf_subset, re.DOTALL)
        matches13 = re.findall(padrao13,  texto_pdf_subset, re.DOTALL)
        matches14 = re.findall(padrao14,  texto_pdf_subset, re.DOTALL)
        matches15 = re.findall(padrao15,  texto_pdf_subset, re.DOTALL)

        for match in matches12:
            # print("controle match 12")
            # print(match)
            pendencias += 1
        for match in matches13:
            # print("controle match 13")
            # print(match)
            pendencias += 1
        for match in matches14:
            # print("controle match 14")
            # print(match)
            pendencias += 1
        for match in matches15:
            # print("controle match 15")
            # print(match)
            pendencias += 1
    
    return pendencias

def count_pendencia_parcelamento_sispar(texto_pdf): #  Parcelamento com Exigibilidade Suspensa (SISPAR)
    padrao1 = r"\b(\d{9})\b"
    matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
    processos = 0
    for match in matches1:
        processos += 1
    
    return processos

def count_pendencia_inscricao_sisdiv(texto_pdf): #Pendência - Inscrição (Sistema DIVIDA)
    padrao1 = r"Inscrição: (\d+-\d) Situação: (\d{6}) - (INSCRICAO DE CREDITO EM DIVIDA ATIVA)"
    end_point = r"Inscrição com Exigibilidade Suspensa \(Sistema DIVIDA\)"
    ini_point = r"Pendência - Inscrição \(Sistema DIVIDA\)"

    ini_match = re.search(ini_point, texto_pdf, re.DOTALL)
    end_match = re.search(end_point, texto_pdf, re.DOTALL)
    processos = 0
    processos_li = []
    if end_match:
        if ini_match and end_match:
            ini_pos = ini_match.end()
            end_pos = end_match.start()

            texto_pdf_subset = texto_pdf[ini_pos:end_pos]
            matches1 = re.findall(padrao1, texto_pdf_subset, re.DOTALL)

            for match in matches1:
                processos_li.append(match[0])
                processos += 1
    else:
        matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)

        for match in matches1:
            processos_li.append(match[0])
            processos += 1
    
    processos_formatados = '\n'.join(processos_li)
    # print(processos_formatados)

    return processos, processos_formatados

def inscricao_exibili_sus_dividida(texto_pdf): #Inscrição com Exigibilidade Suspensa (Sistema DIVIDA)
    padrao1 = r"Inscrição: (\d+-\d) Situação: (\d{6}) - (NEGOCIADO NO SISPAR)"
    ini_point = r"Inscrição com Exigibilidade Suspensa \(Sistema DIVIDA\)"
    end_point = r"Final do Relatório"
    ini_match = re.search(ini_point, texto_pdf, re.DOTALL)
    end_match = re.search(end_point, texto_pdf, re.DOTALL)
    processos = 0
    if end_match:
        if ini_match and end_match:
            ini_pos = ini_match.end()
            end_pos = end_match.start()

            texto_pdf_subset = texto_pdf[ini_pos:end_pos]
            matches1 = re.findall(padrao1, texto_pdf_subset, re.DOTALL)

            for match in matches1:
                processos += 1
    else:
        matches1 = re.findall(padrao1, texto_pdf, re.DOTALL)
        
        for match in matches1:
            processos += 1
    
    return processos


def somar_pendencias_totais(texto_pdf):
    
    total_processos = 0
    processos_sicob, processos_formatados = pednencia_debito_sicob(texto_pdf)
    total_processos += processos_sicob

    processos_fiscal, processos_formatados = count_pendencia_processo_fiscal(texto_pdf)
    total_processos += processos_fiscal

    processos_fiscal_exg = count_pendencia_processo_fiscal_exg(texto_pdf)
    total_processos += processos_fiscal_exg

    processos_sida, processos_formatados = count_pendencia_insc_sida(texto_pdf)
    total_processos += processos_sida

    processos_exig_sus_sida = count_inscricao_exibil_sus_sida(texto_pdf)
    total_processos += processos_exig_sus_sida

    processos_sispar = count_pendencia_parcelamento_sispar(texto_pdf)
    total_processos += processos_sispar

    processos_sisdiv, processos_formatados = count_pendencia_inscricao_sisdiv(texto_pdf)
    total_processos += processos_sisdiv

    processos_exig_sus_dividida = inscricao_exibili_sus_dividida(texto_pdf)
    total_processos += processos_exig_sus_dividida

    processos_formatados = processos_formatados

    return total_processos


@app.route("/", methods=["GET"])
def exibir_formulario():
    return render_template("index.html")

@app.route("/resultado", methods=["POST"])
def processar_formulario():
    arquivo_pdf = request.files["arquivo_pdf"]

    texto_pdf, nome_empresa, cnpj = converter_pdf_para_texto(arquivo_pdf)
    debitos = buscar_valores_debitos(texto_pdf)
    debitos_exigibilidade_suspensa = extrair_debitos_exigibilidade_suspensa(texto_pdf)
    total_debitos_exs = round(sum(debitos_exigibilidade_suspensa.values()), 2)
    total_debitos_exs_formatado = format_currency(total_debitos_exs, "BRL", locale="pt_BR")
    total_debitos = round(sum(debitos.values()), 2)
    total_debitos_formatado = format_currency(total_debitos, "BRL", locale="pt_BR")
    tabela = []
    for nome, valor in debitos.items():
        valor_formatado = format_currency(valor, "BRL", locale="pt_BR")
        tabela.append([nome, valor_formatado])
    
    resultado_table = tabulate(tabela, headers=["Nome do Débito", "Valor"], tablefmt="html")

    tabela_debitos_exs = []
    for nome, valor in debitos_exigibilidade_suspensa.items():
        valor_formatado = format_currency(valor, "BRL", locale="pt_BR")
        tabela_debitos_exs.append([nome, valor_formatado])
    
    resultado_table_exs = tabulate(tabela_debitos_exs, headers=["Nome do débito", "Valor"], tablefmt="html")
    tabela_divergencia, total_debitos_div = pendencia_divergencia(texto_pdf)
    total_debitos_div_for = format_currency(total_debitos_div, "BRL", locale="pt_BR")

    
    processos_fiscal, processos_fiscal_li = count_pendencia_processo_fiscal(texto_pdf)
    # print(f'Quantidade de processos: {processos_fiscal}')
    processos_fiscal_exg = count_pendencia_processo_fiscal_exg(texto_pdf)
    # print(f'Quantidade de processos de exibilidade: {processos_fiscal_exg}')
    processos_parcelamento_sispar = count_pendencia_parcelamento_sispar(texto_pdf)
    # print(f'Quantidade de pendencias parcelamento sispar: {processos_parcelamento_sispar}')
    pendencia_parcelamento_siefpar = count_pendencia_parcelamento_siefpar(texto_pdf)
    pendencia_parcelamento_siefpar_form = format_currency(pendencia_parcelamento_siefpar, "BRL", locale="pt_BR")
    # print(f'pendencia de parcelamento: {pendencia_parcelamento_siefpar_form}')
    pendencia_insc_sida, lista_pendencias = count_pendencia_insc_sida(texto_pdf)
    # print(f'Pendencia de inscrição sida: {pendencia_insc_sida}')
    # print(f'Lista de pendencias da inscrição SIDA: {lista_pendencias}')
    inscricao_exibilidae_sus = count_inscricao_exibil_sus_sida(texto_pdf)
    # print(f'Inscrição com exibilidade suspensa: {inscricao_exibilidae_sus}')
    pendencia_insc_sisdiv, pendencia_insc_sisdiv_li = count_pendencia_inscricao_sisdiv(texto_pdf)
    # print(f'Quantidade de pendencias de inscrição (Sistema DIVIDA): {pendencia_insc_sisdiv}')
    inscricao_exibilidae_sus_dividida = inscricao_exibili_sus_dividida(texto_pdf)
    # print(f'quantidade de inscrições de exibilidade suspensa divididas: {inscricao_exibilidae_sus_dividida}')
    pednencia_sicob, pendencia_sicob_li = pednencia_debito_sicob(texto_pdf)
    pendencia_gfip_li, pendencia_gfip_num = pendencia_omissao_gfip(texto_pdf)
    pendencia_dctfweb_li, pendencia_dctfweb_num  = pendencia_omissao_dctfweb(texto_pdf)
    pendencia_dctf_li, pendencia_dctf_num = pendencia_omissao_dctf(texto_pdf)
    pendencia_efd_li, pendencia_efd_num = pendencia_efd(texto_pdf)
    pendencia_ecf_li, pendencia_ecf_num = pendencia_ecf(texto_pdf)
    pendencia_sipade, pendencia_sipade_li = pendencia_parcelamento_sipade(texto_pdf)
    total_pendencias = somar_pendencias(texto_pdf)
    total_processos = somar_pendencias_totais(texto_pdf)
    data = extrair_data(texto_pdf)
    

    if total_debitos == 0 and total_debitos_div != 0 and total_debitos_exs != 0:
        result = "Empresa livre de débitos"
        # print("controle -3")
        return render_template("resultado.html", tabela=resultado_table, nome_empresa=nome_empresa, cnpj=cnpj, data=data, total_processos=total_processos, result=result, pendencia_ecf_num=pendencia_ecf_num, total_pendencias=total_pendencias, pendencia_efd_num=pendencia_efd_num, pendencia_sipade_li=pendencia_sipade_li, pendencia_dctf_num=pendencia_dctf_num, pendencia_dctfweb_num=pendencia_dctfweb_num, tabela_exigibilidade_suspensa = resultado_table_exs, total_debitos_exigibilidade_suspensa = total_debitos_exs_formatado, tabela_divergencia = tabela_divergencia, pendencia_gfip_num=pendencia_gfip_num, total_debitos_div_for = total_debitos_div_for, processos_fiscal = processos_fiscal, processos_fiscal_exg=processos_fiscal_exg, processos_parcelamento_sispar=processos_parcelamento_sispar, pendencia_parcelamento_siefpar_form = pendencia_parcelamento_siefpar_form, pendencia_insc_sida=pendencia_insc_sida, inscricao_exibilidae_sus=inscricao_exibilidae_sus, pendencia_sipade=pendencia_sipade, pendencia_insc_sisdiv=pendencia_insc_sisdiv, inscricao_exibilidae_sus_dividida=inscricao_exibilidae_sus_dividida, lista_pendencias=lista_pendencias, processos_fiscal_li=processos_fiscal_li, pendencia_insc_sisdiv_li=pendencia_insc_sisdiv_li, pendencia_sicob_li=pendencia_sicob_li, pendencia_gfip_li=pendencia_gfip_li, pendencia_dctfweb_li=pendencia_dctfweb_li, pendencia_dctf_li=pendencia_dctf_li, pendencia_efd_li=pendencia_efd_li, pendencia_ecf_li=pendencia_ecf_li)
    elif total_debitos_div == 0 and total_debitos != 0 and total_debitos_exs != 0:
        result_div = "Empresa livre de débitos"
        # print("controle -2")
        return render_template("resultado.html", tabela=resultado_table, nome_empresa=nome_empresa, cnpj=cnpj, data=data, total_debitos=total_debitos_formatado, total_processos=total_processos, total_pendencias=total_pendencias, pendencia_ecf_num=pendencia_ecf_num, pendencia_efd_num=pendencia_efd_num, pendencia_dctf_num=pendencia_dctf_num, pendencia_sipade_li=pendencia_sipade_li, pendencia_dctfweb_num=pendencia_dctfweb_num, tabela_exigibilidade_suspensa = resultado_table_exs, total_debitos_exigibilidade_suspensa = total_debitos_exs_formatado, result_div=result_div, processos_fiscal = processos_fiscal, pendencia_gfip_num=pendencia_gfip_num, processos_fiscal_exg=processos_fiscal_exg, processos_parcelamento_sispar=processos_parcelamento_sispar, pendencia_parcelamento_siefpar_form = pendencia_parcelamento_siefpar_form, pendencia_insc_sida=pendencia_insc_sida, inscricao_exibilidae_sus=inscricao_exibilidae_sus, pendencia_sipade=pendencia_sipade, pendencia_insc_sisdiv=pendencia_insc_sisdiv, inscricao_exibilidae_sus_dividida=inscricao_exibilidae_sus_dividida, lista_pendencias=lista_pendencias, processos_fiscal_li=processos_fiscal_li, pendencia_insc_sisdiv_li=pendencia_insc_sisdiv_li, pednencia_sicob=pednencia_sicob, pendencia_sicob_li=pendencia_sicob_li, pendencia_gfip_li=pendencia_gfip_li, pendencia_dctfweb_li=pendencia_dctfweb_li, pendencia_dctf_li=pendencia_dctf_li, pendencia_efd_li=pendencia_efd_li, pendencia_ecf_li=pendencia_ecf_li)
    elif total_debitos_exs == 0 and total_debitos_div != 0 and total_debitos != 0:
        result_exs = "Empresa livre de débitos"
        # print("controle -1")
        return render_template("resultado.html", tabela=resultado_table, nome_empresa=nome_empresa, cnpj=cnpj, data=data, total_debitos=total_debitos_formatado, total_processos=total_processos, total_pendencias=total_pendencias, pendencia_ecf_num=pendencia_ecf_num, pendencia_efd_num=pendencia_efd_num, pendencia_dctf_num=pendencia_dctf_num, pendencia_sipade_li=pendencia_sipade_li, pendencia_dctfweb_num=pendencia_dctfweb_num, result_exs=result_exs, tabela_divergencia = tabela_divergencia, total_debitos_div_for = total_debitos_div_for, processos_fiscal = processos_fiscal, processos_fiscal_exg=processos_fiscal_exg, pendencia_gfip_num=pendencia_gfip_num, processos_parcelamento_sispar=processos_parcelamento_sispar, pendencia_parcelamento_siefpar_form = pendencia_parcelamento_siefpar_form, pendencia_insc_sida=pendencia_insc_sida, inscricao_exibilidae_sus=inscricao_exibilidae_sus, pendencia_insc_sisdiv=pendencia_insc_sisdiv, pendencia_sipade=pendencia_sipade, inscricao_exibilidae_sus_dividida=inscricao_exibilidae_sus_dividida, lista_pendencias=lista_pendencias, processos_fiscal_li=processos_fiscal_li, pendencia_insc_sisdiv_li=pendencia_insc_sisdiv_li, pendencia_dctfweb_li=pendencia_dctfweb_li, pendencia_sicob_li=pendencia_sicob_li, pendencia_gfip_li=pendencia_gfip_li, pendencia_dctf_li=pendencia_dctf_li, pendencia_efd_li=pendencia_efd_li, pendencia_ecf_li=pendencia_ecf_li)
    elif ((total_debitos == 0) and (total_debitos_div == 0) and (total_debitos_exs != 0)):
        result = "Empresa livre de débitos"
        result_div = "Empresa livre de débitos"
        # print("controle 0")
        return render_template("resultado.html", tabela=resultado_table, nome_empresa=nome_empresa, cnpj=cnpj, data=data, result=result, total_pendencias=total_pendencias, total_processos=total_processos, pendencia_sipade_li=pendencia_sipade_li, pendencia_ecf_num=pendencia_ecf_num, pendencia_efd_num=pendencia_efd_num, pendencia_dctf_num=pendencia_dctf_num, tabela_exigibilidade_suspensa = resultado_table_exs, pendencia_dctfweb_num=pendencia_dctfweb_num, total_debitos_exigibilidade_suspensa = total_debitos_exs_formatado, result_div=result_div, processos_fiscal = processos_fiscal, pendencia_gfip_num=pendencia_gfip_num, processos_fiscal_exg=processos_fiscal_exg, processos_parcelamento_sispar=processos_parcelamento_sispar, pendencia_parcelamento_siefpar_form = pendencia_parcelamento_siefpar_form, pendencia_insc_sida=pendencia_insc_sida, inscricao_exibilidae_sus=inscricao_exibilidae_sus, pendencia_insc_sisdiv=pendencia_insc_sisdiv, pendencia_sipade=pendencia_sipade, inscricao_exibilidae_sus_dividida=inscricao_exibilidae_sus_dividida, lista_pendencias=lista_pendencias, processos_fiscal_li=processos_fiscal_li, pendencia_insc_sisdiv_li=pendencia_insc_sisdiv_li, pendencia_sicob_li=pendencia_sicob_li, pendencia_gfip_li=pendencia_gfip_li, pendencia_dctfweb_li=pendencia_dctfweb_li, pendencia_dctf_li=pendencia_dctf_li, pendencia_efd_li=pendencia_efd_li, pendencia_ecf_li=pendencia_ecf_li)
    elif total_debitos == 0 and total_debitos_exs == 0 and total_debitos_div != 0:
        result = "Empresa livre de débitos"
        result_exs = "Empresa livre de débitos"
        # print("controle 1")
        return render_template("resultado.html", tabela=resultado_table, nome_empresa=nome_empresa, cnpj=cnpj, data=data, result=result, total_pendencias=total_pendencias, total_processos=total_processos, pendencia_sipade_li=pendencia_sipade_li, pendencia_ecf_num=pendencia_ecf_num, pendencia_efd_num=pendencia_efd_num, pendencia_dctf_num=pendencia_dctf_num, result_exs=result_exs, tabela_divergencia = tabela_divergencia, pendencia_dctfweb_num=pendencia_dctfweb_num, total_debitos_div_for = total_debitos_div_for, processos_fiscal = processos_fiscal, processos_fiscal_exg=processos_fiscal_exg, pendencia_gfip_num=pendencia_gfip_num, processos_parcelamento_sispar=processos_parcelamento_sispar, pendencia_parcelamento_siefpar_form = pendencia_parcelamento_siefpar_form, pendencia_insc_sida=pendencia_insc_sida, inscricao_exibilidae_sus=inscricao_exibilidae_sus, pendencia_insc_sisdiv=pendencia_insc_sisdiv, inscricao_exibilidae_sus_dividida=inscricao_exibilidae_sus_dividida, pendencia_sipade=pendencia_sipade, lista_pendencias=lista_pendencias, processos_fiscal_li=processos_fiscal_li, pendencia_insc_sisdiv_li=pendencia_insc_sisdiv_li, pendencia_sicob_li=pendencia_sicob_li, pendencia_gfip_li=pendencia_gfip_li, pendencia_dctfweb_li=pendencia_dctfweb_li, pendencia_dctf_li=pendencia_dctf_li, pendencia_efd_li=pendencia_efd_li, pendencia_ecf_li=pendencia_ecf_li)
    elif total_debitos_div == 0 and total_debitos_exs == 0 and total_debitos != 0:  
        result_div = "Empresa livre de débitos"
        result_exs = "Empresa livre de débitos"
        # print("controle 2")
        return render_template("resultado.html", tabela=resultado_table, nome_empresa=nome_empresa, cnpj=cnpj, data=data, total_pendencias=total_pendencias, total_processos=total_processos, total_debitos=total_debitos_formatado, pendencia_ecf_num=pendencia_ecf_num, pendencia_efd_num=pendencia_efd_num, pendencia_dctf_num=pendencia_dctf_num, pendencia_sipade_li=pendencia_sipade_li, result_exs=result_exs, result_div=result_div, pendencia_dctfweb_num=pendencia_dctfweb_num, processos_fiscal = processos_fiscal, processos_fiscal_exg=processos_fiscal_exg, processos_parcelamento_sispar=processos_parcelamento_sispar, pendencia_gfip_num=pendencia_gfip_num, pendencia_parcelamento_siefpar_form = pendencia_parcelamento_siefpar_form, pendencia_insc_sida=pendencia_insc_sida, inscricao_exibilidae_sus=inscricao_exibilidae_sus, pendencia_insc_sisdiv=pendencia_insc_sisdiv, inscricao_exibilidae_sus_dividida=inscricao_exibilidae_sus_dividida, lista_pendencias=lista_pendencias, pendencia_sipade=pendencia_sipade, processos_fiscal_li=processos_fiscal_li, pendencia_insc_sisdiv_li=pendencia_insc_sisdiv_li,pendencia_ecf_li=pendencia_ecf_li, pendencia_sicob_li=pendencia_sicob_li, pendencia_gfip_li=pendencia_gfip_li, pendencia_dctfweb_li=pendencia_dctfweb_li, pendencia_dctf_li=pendencia_dctf_li, pendencia_efd_li=pendencia_efd_li)
    elif total_debitos == 0 and total_debitos_div == 0 and total_debitos_exs == 0:
        result_div = "Empresa livre de débitos"
        result_exs = "Empresa livre de débitos"
        result = "Empresa livre de débitos"
        # print("controle 3")
        return render_template("resultado.html", nome_empresa=nome_empresa, cnpj=cnpj, result=result, result_exs=result_exs, data=data, total_pendencias=total_pendencias, total_processos=total_processos, result_div=result_div, pendencia_ecf_num=pendencia_ecf_num, pendencia_efd_num=pendencia_efd_num, pendencia_dctf_num=pendencia_dctf_num, pendencia_sipade_li=pendencia_sipade_li, processos_fiscal = processos_fiscal, pendencia_dctfweb_num=pendencia_dctfweb_num, processos_fiscal_exg=processos_fiscal_exg, processos_parcelamento_sispar=processos_parcelamento_sispar, pendencia_parcelamento_siefpar_form = pendencia_parcelamento_siefpar_form, pendencia_gfip_num=pendencia_gfip_num, pendencia_insc_sida=pendencia_insc_sida, inscricao_exibilidae_sus=inscricao_exibilidae_sus, pendencia_insc_sisdiv=pendencia_insc_sisdiv, inscricao_exibilidae_sus_dividida=inscricao_exibilidae_sus_dividida, pendencia_sipade=pendencia_sipade, lista_pendencias=lista_pendencias, processos_fiscal_li=processos_fiscal_li, pendencia_insc_sisdiv_li=pendencia_insc_sisdiv_li, pendencia_sicob_li=pendencia_sicob_li, pendencia_gfip_li=pendencia_gfip_li, pendencia_dctfweb_li=pendencia_dctfweb_li, pendencia_dctf_li=pendencia_dctf_li, pendencia_efd_li=pendencia_efd_li, pendencia_ecf_li=pendencia_ecf_li)
    else:
        # print("controle else")
        return render_template("resultado.html",  tabela=resultado_table, nome_empresa=nome_empresa, cnpj=cnpj, data=data, total_pendencias=total_pendencias, total_processos=total_processos, total_debitos=total_debitos_formatado, pendencia_ecf_num=pendencia_ecf_num, pendencia_efd_num=pendencia_efd_num, pendencia_dctf_num=pendencia_dctf_num, pendencia_sipade_li=pendencia_sipade_li, tabela_exigibilidade_suspensa = resultado_table_exs, pendencia_dctfweb_num=pendencia_dctfweb_num, total_debitos_exigibilidade_suspensa = total_debitos_exs_formatado, tabela_divergencia = tabela_divergencia, pendencia_gfip_num=pendencia_gfip_num, total_debitos_div_for = total_debitos_div_for, processos_fiscal = processos_fiscal, processos_fiscal_exg=processos_fiscal_exg, processos_parcelamento_sispar=processos_parcelamento_sispar, pendencia_parcelamento_siefpar_form = pendencia_parcelamento_siefpar_form, pendencia_sipade=pendencia_sipade, pendencia_insc_sida=pendencia_insc_sida, inscricao_exibilidae_sus=inscricao_exibilidae_sus, pendencia_insc_sisdiv=pendencia_insc_sisdiv, inscricao_exibilidae_sus_dividida=inscricao_exibilidae_sus_dividida, lista_pendencias=lista_pendencias, processos_fiscal_li=processos_fiscal_li, pendencia_insc_sisdiv_li=pendencia_insc_sisdiv_li, pendencia_dctf_li=pendencia_dctf_li, pendencia_efd_li=pendencia_efd_li, pendencia_sicob_li=pendencia_sicob_li, pendencia_gfip_li=pendencia_gfip_li, pendencia_dctfweb_li=pendencia_dctfweb_li, pendencia_ecf_li=pendencia_ecf_li)


if __name__ == "__main__":
    app.run(debug=True, port=port)