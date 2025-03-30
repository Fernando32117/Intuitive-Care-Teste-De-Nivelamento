import ftplib  # Importa a biblioteca para conexão com FTP
import os      # Importa a biblioteca para manipulação de diretórios e arquivos

def baixar_arquivos_ftp_demonstracoes():  
    """  
    Função que acessa o servidor FTP e baixa os arquivos das pastas de 2023 e 2024.  
    """  
    ftp_host = "dadosabertos.ans.gov.br" # Endereço do servidor FTP  
    destino_pasta = "downloads_ftp"      # Pasta onde os arquivos serão salvos  
    
    # Verifica se a pasta de destino existe, senão cria  
    if not os.path.exists(destino_pasta):  
        os.makedirs(destino_pasta)  
    
    ftp = ftplib.FTP(ftp_host)  # Conecta ao servidor FTP  
    ftp.login()                 # Faz login (acesso anônimo, pois não tem usuário/senha)  
    
    anos = ["2023", "2024"] # Lista de anos cujos arquivos queremos baixar  
    
    arquivos_baixados = []  # Lista para armazenar os arquivos baixados  
    
    for ano in anos:  
        diretorio_remoto = f"/FTP/PDA/demonstracoes_contabeis/{ano}"  # Caminho da pasta no FTP
        
        try:  
            ftp.cwd(diretorio_remoto)  # Muda para o diretório do ano no servidor FTP  
            
            subpasta_ano = os.path.join(destino_pasta, ano)  # Define a pasta local para armazenar os arquivos  
            if not os.path.exists(subpasta_ano):  
                os.makedirs(subpasta_ano)  # Cria a pasta caso não exista  
            
            arquivos = ftp.nlst()  # Lista os arquivos disponíveis no diretório remoto  
            
            for arquivo in arquivos:  # Loop para baixar cada arquivo  
                caminho_local = os.path.join(subpasta_ano, arquivo)  # Caminho completo onde o arquivo será salvo  
                with open(caminho_local, "wb") as f:  # Abre o arquivo local no modo de escrita binária  
                    ftp.retrbinary(f"RETR {arquivo}", f.write)  # Baixa o arquivo e escreve no local  
                    print(f"Arquivo {arquivo} baixado com sucesso em {subpasta_ano}.")  
                    arquivos_baixados.append(caminho_local)  # Adiciona o arquivo à lista de baixados  
        
        except ftplib.error_perm as e:  
            print(f"Erro ao acessar o diretório {diretorio_remoto}: {e}")  # Exibe erro caso não consiga acessar a pasta  

    ftp.quit()  # Fecha a conexão com o FTP  
    return arquivos_baixados  # Retorna a lista de arquivos baixados  

def baixar_dados_cadastrais_operadoras():  
    """  
    Função que acessa o servidor FTP e baixa os dados cadastrais das operadoras ativas.  
    """  
    ftp_host = "dadosabertos.ans.gov.br"        # Endereço do servidor FTP  
    destino_pasta = "downloads_ftp/operadoras"  # Define a pasta onde os arquivos serão salvos  
    
    # Verifica se a pasta existe, se não, cria  
    if not os.path.exists(destino_pasta):  
        os.makedirs(destino_pasta)  
    
    ftp = ftplib.FTP(ftp_host)  # Conecta ao FTP  
    ftp.login()  # Faz login no FTP  
    
    diretorio_operadoras = "/FTP/PDA/operadoras_de_plano_de_saude_ativas"  # Diretório onde os arquivos estão armazenados  
    
    try:  
        ftp.cwd(diretorio_operadoras)  # Muda para o diretório das operadoras  
        arquivos = ftp.nlst()  # Lista os arquivos disponíveis no diretório remoto  
        
        for arquivo in arquivos:  
            # Filtra apenas arquivos CSV (evita baixar arquivos desnecessários)  
            if arquivo.endswith('.csv'):  
                caminho_local = os.path.join(destino_pasta, arquivo)  # Define o caminho onde o arquivo será salvo  
                with open(caminho_local, "wb") as f:  # Abre o arquivo no modo binário  
                    ftp.retrbinary(f"RETR {arquivo}", f.write)  # Baixa o arquivo do FTP e escreve no local  
                    print(f"Arquivo {arquivo} baixado com sucesso em {destino_pasta}.")  
    
    except ftplib.error_perm as e:  
        print(f"Erro ao acessar o diretório {diretorio_operadoras}: {e}")  # Mensagem de erro caso o diretório não exista  

    ftp.quit()  # Fecha a conexão com o FTP  

if __name__ == "__main__":  
    # Baixa os arquivos dos demonstrativos  
    arquivos_baixados_demonstrações = baixar_arquivos_ftp_demonstracoes()  
    
    if arquivos_baixados_demonstrações:  
        print("Todos os arquivos dos demonstrativos foram baixados com sucesso.")  
    
    # Baixa os dados cadastrais das operadoras  
    baixar_dados_cadastrais_operadoras()  
