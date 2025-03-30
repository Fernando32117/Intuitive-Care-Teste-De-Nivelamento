import os  
import pandas as pd  
from flask import Flask, request, jsonify  
from flask_cors import CORS  

app = Flask(__name__)  
CORS(app)  

# Aqui a gente obtém o caminho absoluto do arquivo. Isso é pra garantir que vamos acessar o CSV certo.  
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))   
csv_path = os.path.join(BASE_DIR, "..", "TESTE-DE-BANCO-DE-DADOS", "downloads_ftp", "operadoras", "Relatorio_cadop.csv")  

# Vamos checar se o caminho do arquivo CSV tá certo. Se não estiver, a gente vai dar um erro e avisar.  
print(f"Verificando o caminho do arquivo CSV: {csv_path}")  
if not os.path.exists(csv_path):  
    raise FileNotFoundError(f"O arquivo CSV não foi encontrado no caminho: {csv_path}")  

# Agora é hora de carregar o CSV pra dentro do pandas !  
df = pd.read_csv(csv_path, sep=";", na_filter=True, on_bad_lines="warn")  

# Aqui estamos limpando os nomes das colunas, tirando espaços extras !  
df.columns = df.columns.str.strip()  

# Se a coluna com a data existir, vamos transformar o formato dela. Isso é importante pra análise!  
if 'data_registro_ans' in df.columns:  
    df['data_registro_ans'] = pd.to_datetime(df['data_registro_ans'], errors='coerce')  

@app.route('/search', methods=['GET'])  
def search():  
    query = request.args.get('query')  
    
    if query:  
        # Aqui a gente cria uma máscara pra filtrar as colunas que têm a busca, essencial pra encontrar o que queremos.  
        mask = df.apply(lambda column: column.astype(str).str.contains(query, case=False, na=False))  
        results = df[mask.any(axis=1)]  # Retorna todas as linhas que tiverem algo em qualquer coluna que bate com a busca  

        # Agora vamos pegar só as colunas que realmente queremos  
        results_dict = results[['Registro_ANS', 'CNPJ', 'Razao_Social', 'Nome_Fantasia', 'Modalidade', 'Logradouro',  
                                 'Numero', 'Complemento', 'Bairro', 'Cidade', 'UF', 'CEP',   
                                 'DDD', 'Telefone', 'Endereco_eletronico', 'Representante',   
                                 'Cargo_Representante', 'Data_Registro_ANS']].where(pd.notnull(results), None).to_dict(orient='records')  

        # Aqui a gente se certifica de que não tá retornando valores inválidos!  
        results_dict = [{k: (v if not isinstance(v, float) or not pd.isna(v) else None) for k, v in record.items()} for record in results_dict]  

        print("Resultados da busca:", results_dict)  
        return jsonify(results_dict)  
    
    return jsonify([])  # Se não teve consulta, retorna uma lista vazia   

if __name__ == '__main__':  
    app.run(debug=True)  # E aqui, rodamos a aplicação em modo debug  