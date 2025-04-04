from dotenv import load_dotenv  
import psycopg2  
import csv   
import os   

# Carrega variáveis do arquivo .env  
load_dotenv()  

# Obtendo credenciais do banco de dados  
host = os.getenv('DB_HOST')  
user = os.getenv('DB_USER')  
password = os.getenv('DB_PASSWORD')  
dbname = os.getenv('DB_NAME') 

# Inicialização das variáveis  
conn = None  
cursor = None   

# Função para criar o banco de dados  
def create_database(dbname):  
    # Conectando à instância do PostgreSQL sem um banco de dados específico  
    connection = psycopg2.connect(  
        host=host,  
        user=user,  
        password=password  
    )  
    connection.autocommit = True   
    cursor = connection.cursor()  
    
    # SQL para criar o banco de dados se não existir  
    create_db_query = f"CREATE DATABASE {dbname};"  
    
    try:  
        cursor.execute(create_db_query)  
        print(f"Banco de dados '{dbname}' criado com sucesso!")  
    except psycopg2.errors.DuplicateDatabase:  
        print(f"O banco de dados '{dbname}' já existe.")  
    finally:  
        cursor.close()  
        connection.close()  

# Criar o banco de dados se não existir  
try:  
    create_database(dbname)  
    
    # Agora tente conectar ao banco de dados recém-criado  
    conn = psycopg2.connect(  
        host=host,  
        dbname=dbname,  
        user=user,  
        password=password,  
        options="-c client_encoding=utf8"  
    )  
    print("Conexão ao banco de dados bem-sucedida!")  
    
    # Criação de um cursor  
    cursor = conn.cursor()  

    # SQL para criar a tabela operadoras se não existir  
    create_operadoras_table_query = '''  
    CREATE TABLE IF NOT EXISTS operadoras (  
        registro_operadora VARCHAR(6) PRIMARY KEY,
        cnpj VARCHAR(14) UNIQUE NOT NULL,
        razao_social VARCHAR(140),
        nome_fantasia VARCHAR(140),
        modalidade VARCHAR(50),
        logradouro VARCHAR(40),
        numero VARCHAR(20),
        complemento VARCHAR(40),
        bairro VARCHAR(30),
        cidade VARCHAR(30),
        uf CHAR(2),
        cep VARCHAR(8),
        ddd VARCHAR(4),
        telefone VARCHAR(20),
        fax VARCHAR(20),
        endereco_eletronico VARCHAR(255),
        representante VARCHAR(50),
        cargo_representante VARCHAR(40),
        regiao_de_comercializacao SMALLINT CHECK (regiao_de_comercializacao BETWEEN 1 AND 6),
        data_registro_ans DATE NOT NULL
    );  
    '''  
    # Executar a query de criação de tabela operadoras  
    cursor.execute(create_operadoras_table_query)  
    conn.commit()  
    print("Tabela 'operadoras' criada ou já existe!")    

    # Caminho para o arquivo CSV  
    csv_file_path = 'downloads_ftp/operadoras/Relatorio_cadop.csv'

    # Importar o conteúdo do arquivo CSV  
    with open(csv_file_path, 'r', encoding='utf-8') as f:  
        reader = csv.reader(f, delimiter=';')  
        header = next(reader)  # Ignorar o cabeçalho  

        for row in reader:  
            # Lê os dados do CSV e converte valores vazios para None
            registro_operadora = row[0] if row[0] else None
            cnpj = row[1] if row[1] else None
            razao_social = row[2] if row[2] else None
            nome_fantasia = row[3] if row[3] else None
            modalidade = row[4] if row[4] else None
            logradouro = row[5] if row[5] else None
            numero = row[6] if row[6] else None
            complemento = row[7] if row[7] else None
            bairro = row[8] if row[8] else None
            cidade = row[9] if row[9] else None
            uf = row[10] if row[10] else None
            cep = row[11] if row[11] else None
            ddd = row[12] if row[12] else None
            telefone = row[13] if row[13] else None
            fax = row[14] if row[14] else None
            endereco_eletronico = row[15] if row[15] else None
            representante = row[16] if row[16] else None
            cargo_representante = row[17] if row[17] else None
            regiao_de_comercializacao = int(row[18]) if row[18] else None
                    
            # Convertendo data para formato PostgreSQL (YYYY-MM-DD)
            data_registro_ans = row[19] if row[19] else None
            if data_registro_ans:
                data_registro_ans = data_registro_ans.replace('/', '-')  # Substitui '/' por '-'
        
            # Inserir os dados na tabela
            cursor.execute('''
                INSERT INTO operadoras (registro_operadora, cnpj, razao_social, nome_fantasia, modalidade,  
                                       logradouro, numero, complemento, bairro, cidade, uf, cep,  
                                       ddd, telefone, fax, endereco_eletronico, representante,  
                                       cargo_representante, regiao_de_comercializacao, data_registro_ans)  
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (registro_operadora) DO NOTHING
            ''', (
                registro_operadora, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep,
                ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_de_comercializacao, data_registro_ans
            ))  

    conn.commit()  
    print("Dados importados com sucesso do 'Relatorio_cadop.csv' !")
    
    # SQL para criar a tabela despesas se não existir  
    create_despesas_table_query = '''  
    CREATE TABLE IF NOT EXISTS despesas (  
        data DATE NOT NULL,
        reg_ans BIGINT NOT NULL,
        cd_conta_contabil BIGINT NOT NULL,
        descricao VARCHAR(150) NOT NULL,
        vl_saldo_inicial NUMERIC(15, 2),
        vl_saldo_final NUMERIC(15, 2) 
    );  
    ''' 
    # Executar a query de criação de tabela despesas  
    cursor.execute(create_despesas_table_query)  
    conn.commit()  
    print("Tabela 'despesas' criada ou já existe!")

except Exception as e:  
    print(f"Ocorreu um erro: {e}")  

finally:  
    # Fechar o cursor e a conexão, se existirem  
    if cursor is not None:  
        cursor.close()  
    if conn is not None:  
        conn.close()  
        print("Conexão ao banco de dados fechada.")  