-- Quais as 10 operadoras com maiores despesas no último ano

SELECT   
    o.nome_fantasia,   
    SUM(d.vl_saldo_final) AS total_despesas  
FROM   
    despesas d  
JOIN   
    operadoras o ON d.reg_ans = o.registro_ans  
WHERE   
    d.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'  
    AND d.data >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year' 
GROUP BY   
    o.nome_fantasia  
ORDER BY   
    total_despesas DESC  
LIMIT 10;