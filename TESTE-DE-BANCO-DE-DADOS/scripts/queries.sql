-- 3.3: Criação da tabela para armazenar os dados das operadoras  
CREATE TABLE operadoras (
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
    regiao_de_comercializacao SMALLINT CHECK (
        regiao_de_comercializacao BETWEEN 1 AND 6
    ),
    data_registro_ans DATE
);

-- Criação da tabela para armazenar as despesas 

CREATE TABLE despesas (
    data DATE NOT NULL,
    reg_ans BIGINT NOT NULL,
    cd_conta_contabil BIGINT NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    vl_saldo_inicial NUMERIC(15, 2),
    vl_saldo_final NUMERIC(15, 2)
);

-- 3.4: Importando o conteúdo do arquivo CSV para a tabela operadoras  
COPY operadoras(
    registro_operadora,
    cnpj,
    razao_social,
    nome_fantasia,
    modalidade,
    logradouro,
    numero,
    complemento,
    bairro,
    cidade,
    uf,
    cep,
    ddd,
    telefone,
    fax,
    endereco_eletronico,
    representante,
    cargo_representante,
    regiao_de_comercializacao,
    data_registro_ans
)
FROM 'downloads_ftp/operadoras/Relatorio_cadop.csv' WITH (
        FORMAT csv,
        DELIMITER ';',
        HEADER true,
        ENCODING 'UTF8'
    );