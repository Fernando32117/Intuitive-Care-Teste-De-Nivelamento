-- 3.3: Criação da tabela para armazenar os dados das operadoras  
CREATE TABLE operadoras (  
    id SERIAL PRIMARY KEY,  
    registro_ans VARCHAR(20),  
    cnpj VARCHAR(14) UNIQUE,  
    razao_social VARCHAR(255),  
    nome_fantasia VARCHAR(255),  
    modalidade VARCHAR(50),  
    logradouro VARCHAR(100),  
    numero VARCHAR(10),  
    complemento VARCHAR(50),  
    bairro VARCHAR(50),  
    cidade VARCHAR(50),  
    uf VARCHAR(2),  
    cep VARCHAR(10),  
    ddd VARCHAR(3),  
    telefone VARCHAR(15),  
    fax VARCHAR(15),  
    endereco_eletronico VARCHAR(100),  
    representante VARCHAR(100),  
    cargo_representante VARCHAR(100),  
    regiao_de_comercializacao VARCHAR(50),  
    data_registro_ans DATE  
);  

-- 3.4: Criação da tabela para armazenar as despesas  
CREATE TABLE despesas (
    id SERIAL PRIMARY KEY,
    data DATE,
    reg_ans VARCHAR(20),
    cd_conta_contabil VARCHAR(255),
    descricao VARCHAR(255),
    vl_saldo_inicial DECIMAL(15, 2), 
    vl_saldo_final DECIMAL(15, 2),
    FOREIGN KEY (reg_ans) REFERENCES operadoras(registro_ans)
);     

-- Importando o conteúdo do arquivo CSV para a tabela operadoras  
COPY operadoras(registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_de_comercializacao, data_registro_ans)  
FROM '/caminho/para/Relatorio_cadop.csv'   
WITH (FORMAT csv, DELIMITER ';', HEADER true, ENCODING 'UTF8');  