<template>
  <div id="app">
    <h1>Busca de Operadoras de Saúde </h1>
    <img src="./assets/logo2.png" alt="" class="img">
    <div class="search-container">
      <input v-model="query" placeholder="Buscar operadora..." class="search-input" />
      <button @click="search" class="search-button">Buscar</button>
    </div>
    <ul class="search-results">
      <h2>Resultado da Busca</h2>
      <li v-for="item in results" :key="item.Registro_ANS" class="result-item">
        <h3 class="result-title">{{ item.Razao_Social || 'Nome não disponível' }}</h3>
        <p><strong>CNPJ:</strong> {{ item.CNPJ || 'Não informado' }}</p>
        <p><strong>Nome Fantasia:</strong> {{ item.Nome_Fantasia || 'Não informado' }}</p>
        <p><strong>Modalidade:</strong> {{ item.Modalidade || 'Não informada' }}</p>
        <p><strong>Endereço:</strong> {{ item.Logradouro || '' }} {{ item.Numero || '' }} {{ item.Complemento || ''
        }}<br />
          {{ item.Bairro || '' }} - {{ item.Cidade || '' }} - {{ item.UF || '' }} - {{ item.CEP || '' }}</p>
        <p><strong>Telefone:</strong> {{ item.Telefone || 'Não informado' }}</p>
        <p><strong>Email:</strong> <a v-if="item.Endereco_eletronico" :href="`mailto:${item.Endereco_eletronico}`">{{
          item.Endereco_eletronico }}</a></p>
        <p><strong>Representante:</strong> {{ item.Representante || 'Não informado' }} - {{ item.Cargo_Representante ||
          'Cargo não disponível' }}</p>
        <p><strong>Data de Registro:</strong> {{ item.Data_Registro_ANS || 'Não informada' }}</p>
      </li>
    </ul>
    <div v-if="results.length === 0">
      <p>Nenhum resultado encontrado até o momento !</p>
    </div>
  </div>
</template>

<style scoped>
#app {
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(0, 0, 0, 0.2));
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(10px);
}

.img {
  display: block;
  margin: 30px auto;
  width: 100%;
  max-width: 500px;
  height: auto;
  border: 4px solid rgb(107, 57, 168);
  border-radius: 10px;
  padding: 5px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

h1 {
  text-align: center;
  color: rgb(107, 57, 168);
  font-size: 2.2rem;
}

p {
  color: #555;
  font-size: 1rem;
}

.search-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-input {
  width: 70%;
  padding: 10px;
  border: 1px solid rgb(107, 57, 168);
  border-radius: 5px;
  margin-right: 10px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: rgb(107, 57, 168);
  outline: none;
}

.search-button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  background-color: rgb(107, 57, 168);
  color: white;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: rgb(200, 164, 244);
}

h2 {
  text-align: center;
  color: rgb(200, 164, 244);
  margin-top: 30px;
  font-size: 1.5rem;
}

.search-results {
  list-style-type: none;
  padding: 0;
}

.result-item {
  background: linear-gradient(110deg, rgba(255, 255, 255, 0.2), rgba(0, 0, 0, 0.2));
  margin: 15px 0;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

.result-item:hover {
  background-color: rgba(200, 164, 244, 0.3);
}

.result-title {
  margin: 0;
  font-size: 1.3rem;
  color: rgb(107, 57, 168);
}

strong {
  color: rgb(0, 0, 0);
}

/* Responsividade para telas menores */
@media screen and (max-width: 768px) {
  #app {
    max-width: 90%;
    padding: 15px;
  }

  .img {
    width: 90%;
    height: auto;
  }

  h1 {
    font-size: 1.8rem;
  }

  h2 {
    font-size: 1.3rem;
  }

  p {
    font-size: 0.9rem;
  }

  .search-container {
    flex-direction: column;
    align-items: center;
  }

  .search-input {
    max-width: 90%;
    margin-right: 0;
    margin-bottom: 10px;
  }

  .search-button {
    max-width: 90%;
  }

  .result-title {
    font-size: 1.2rem;
  }
}
</style>


<script>
export default {
  data() {
    return {
      query: '',
      results: []
    };
  },
  methods: {
    async search() {
      try {
        const response = await fetch(`http://localhost:5000/search?query=${this.query}`);

        // Verifica se a resposta não é OK (status != 200)  
        if (!response.ok) {
          throw new Error(`Erro: ${response.status} ${response.statusText}`); // Lança um erro com uma mensagem customizada  
        }

        this.results = await response.json();
        console.log("Resultados retornados:");
        console.table(this.results); // Exibe resultados em formato de tabela  
        console.log(`Total de resultados: ${this.results.length}`);

      } catch (error) {
        // Captura qualquer erro de rede ou erro customizado  
        console.error("Erro ao buscar resultados:", error.message);  
        alert(`Não foi possível buscar os resultados: ${error.message}`);
      }
    }
  }
}  
</script>