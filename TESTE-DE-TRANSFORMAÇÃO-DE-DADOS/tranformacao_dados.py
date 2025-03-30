import pdfplumber    # Biblioteca pra trabalhar com PDFs e extrair dados  
import pandas as pd  # Usada pra manipulação de dados e tabelas  
import zipfile       # Biblioteca pra criar arquivos ZIP  
import os            # Usada pra manipulação de diretórios e arquivos  

# Caminho do arquivo PDF que a gente vai ler  
pdf_path = "../TESTE-DE-WEB-SCRAPING/downloads/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"  
csv_filename = "resultados/dados_transformados.csv"       # Nome do arquivo CSV que vamos criar  
zip_filename = "resultados/Teste_francisco_fernando.zip"  # Nome do arquivo ZIP que vamos gerar  

# Mapeamento das abreviações para substituir depois  
abreviacoes = {  
    "OD": " Seg. Odontológica",  
    "AMB": "Seg. Ambulatorial"  
}  

def extrair_dados_do_pdf(pdf_path):  
    """Extrai as tabelas do PDF e retorna uma lista de DataFrames"""  
    tabelas = []                                     # Lista onde vamos guardar as tabelas que extrair  
    with pdfplumber.open(pdf_path) as pdf:           # Abre o PDF  
        for page in pdf.pages:                       # Para cada página do PDF  
            table = page.extract_table()             # Tenta extrair a tabela da página  
            if table:                                # Se conseguiu extrair a tabela  
                tabelas.append(pd.DataFrame(table))  # Adiciona a tabela à lista como um DataFrame  
    return tabelas  

def salvar_como_csv(tabelas, csv_filename):  
    """Salva os dados extraídos em um único arquivo CSV"""  
    
    # Cria a pasta onde vamos salvar o CSV se não existir  
    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)  
    
    df_final = pd.concat(tabelas, ignore_index=True)  # Junta todas as tabelas em um só DataFrame  
    
    # Renomeia as colunas com a primeira linha do DataFrame  
    df_final.columns = df_final.iloc[0]  # Define a primeira linha como cabeçalho  
    df_final = df_final[1:]              # Remove a linha duplicada do cabeçalho  
    
    # Substitui as abreviações pelas strings completas  
    df_final.replace(abreviacoes, inplace=True)  
    
    df_final.to_csv(csv_filename, index=False)   # Salva o DataFrame como CSV  
    print(f"Arquivo CSV salvo: {csv_filename}")  # Mensagem de confirmação  

def compactar_csv(csv_filename, zip_filename):  
    """Compacta o arquivo CSV em um arquivo ZIP"""  
    
    # Cria a pasta para o ZIP se não existir  
    os.makedirs(os.path.dirname(zip_filename), exist_ok=True)  
    
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:  
        zipf.write(csv_filename, os.path.basename(csv_filename))  # Adiciona o CSV ao ZIP  
    print(f"Arquivo compactado: {zip_filename}")                  # Mensagem de confirmação  

if __name__ == "__main__":  
    tabelas_extraidas = extrair_dados_do_pdf(pdf_path)    # Chama a função pra extrair os dados do PDF  
    if tabelas_extraidas:                                 # Se a gente conseguiu extrair tabelas  
        salvar_como_csv(tabelas_extraidas, csv_filename)  # Salva as tabelas como CSV  
        compactar_csv(csv_filename, zip_filename)         # E compacta o CSV em ZIP  