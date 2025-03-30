import requests                # Aqui a gente importa a biblioteca pra fazer requisições HTTP  
from bs4 import BeautifulSoup  # Importa a BeautifulSoup pra ajudar a analisar o HTML da página  
import os                      # Biblioteca que ajuda a manipular diretórios e arquivos  
import zipfile                 # Serve pra criar arquivos ZIP  

def baixar_pdfs():  
    """  
    Função que acessa uma página web, pega os links de PDFs com "Anexo" no nome  
    e baixa esses arquivos pra pasta 'downloads'.  
    """  
    # URL da página onde estão os PDFs que queremos  
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"  
    
    # Faz uma requisição GET pra pegar o conteúdo da página  
    response = requests.get(url)  
    
    # Se deu algum erro na requisição, isso vai levantar um erro pra gente  
    response.raise_for_status()  
    
    # Analisa o HTML da página com a BeautifulSoup  
    soup = BeautifulSoup(response.text, 'html.parser')  
    
    # Aqui a gente encontra todas as tags <a> que têm um atributo 'href' (ou seja, links)  
    links = soup.find_all('a', href=True)  
    
    # Filtra os links que terminam com ".pdf" e têm "Anexo" no texto  
    pdf_links = [link['href'] for link in links if link['href'].endswith(".pdf") and "Anexo" in link.text]  
    
    # Cria a pasta "downloads" se ela ainda não existir  
    if not os.path.exists("downloads"):  
        os.makedirs("downloads")  
    
    arquivos_baixados = []  # Lista pra guardar os nomes dos arquivos que a gente baixou  
    
    # Percorre todos os links de PDF encontrados  
    for pdf_link in pdf_links:  
        # Se o link já for completo (começa com "http"), a gente usa ele direto.  
        # Se não, acrescenta a URL da página  
        pdf_url = pdf_link if pdf_link.startswith("http") else url + pdf_link  
        
        # Define onde vamos salvar o arquivo na pasta "downloads"  
        pdf_nome = os.path.join("downloads", pdf_url.split("/")[-1])  
        
        # Abre o arquivo no modo de escrita binária "wb"  
        with open(pdf_nome, "wb") as f:  
            pdf_response = requests.get(pdf_url)  # Faz o download do PDF  
            pdf_response.raise_for_status()       # Verifica se o download deu certo  
            f.write(pdf_response.content)         # Escreve o conteúdo do PDF no arquivo  
            arquivos_baixados.append(pdf_nome)    # Adiciona o nome do arquivo à lista  

    return arquivos_baixados  # Retorna a lista com os nomes dos arquivos baixados  

def compactar_arquivos(arquivos, zip_name="downloads/anexos.zip"):  
    """  
    Função que compacta os arquivos que a gente baixou em um único arquivo ZIP.  
    """  
    with zipfile.ZipFile(zip_name, "w") as zipf:  
        # Adiciona cada arquivo baixado ao arquivo ZIP  
        for arquivo in arquivos:  
            zipf.write(arquivo, os.path.basename(arquivo))  # Salva só o nome do arquivo no ZIP  
    
    print(f"Arquivos compactados em {zip_name}")  # Mostra uma mensagem de confirmação  

if __name__ == "__main__":  
    """  
    Bloco principal do script: chama as funções pra baixar os PDFs e compactá-los se tiver arquivos.  
    """  
    arquivos = baixar_pdfs()  # Chama a função que baixa os PDFs  
    
    if arquivos:  # Se a gente tiver baixado arquivos, compacta eles  
        compactar_arquivos(arquivos)  