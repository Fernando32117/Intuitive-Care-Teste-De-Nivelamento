-- Quais as 10 operadoras com maiores despesas no último trimestre 

SELECT   
    o.nome_fantasia,   
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS total_despesas  
FROM   
    despesas d  
JOIN   
    operadoras o ON d.reg_ans = o.registro_operadora  
WHERE   
    TRIM(d.descricao) = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'  
    AND d.data >= CURRENT_DATE - INTERVAL '3 months'  
GROUP BY   
    o.nome_fantasia  
ORDER BY   
    total_despesas DESC  
LIMIT 10;

