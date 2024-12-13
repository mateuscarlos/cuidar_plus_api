# Cuidar+ API

**Cuidar+ API** é o backend da aplicação Cuidar+, um software em desenvolvimento para o segmento de Home Care. Ele fornece as APIs necessárias para a gestão de pacientes, insumos/medicamentos e acompanhamento de equipes e pacientes. Este repositório é exclusivo para o backend da aplicação.

O frontend do projeto está disponível em [Cuidar+ Frontend](https://github.com/mateuscarlos/cuidar_plus).

## Índice
- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Executar](#como-executar)
- [Verificação das APIs](#verificação-das-apis)
- [Licença](#licença)

---

## Sobre o Projeto

A API do Cuidar+ fornece funcionalidades para:

- **Gestão de Pacientes**:
  - Cadastro, consulta e edição de dados.
  - Acompanhamento do histórico de atendimentos.

- **Gestão de Insumos e Medicamentos**:
  - Controle de estoque.
  - Relatórios de consumo e reabastecimento.

- **Relatórios e Análises**:
  - Geração de relatórios periódicos.
  - KPIs para suporte à tomada de decisão.

---

## Tecnologias Utilizadas

- **Linguagem**: [Python](https://www.python.org)
- **Framework Web**: [Flask](https://flask.palletsprojects.com)
- **Documentação de APIs**: [Flasgger (Swagger)](https://github.com/flasgger/flasgger)
- **Banco de Dados**: [SQLite](https://sqlite.org/index.html)

---

## Como Executar

### Pré-requisitos

- [Python 3.8+](https://www.python.org/downloads/)
- Gerenciador de pacotes `pip`
- Ambiente virtual (recomendado)

### Passos

1. **Clone os repositórios do projeto:**
   ```bash
   mkdir projeto-cuidar
   cd projeto-cuidar
   git clone https://github.com/mateuscarlos/cuidar_plus.git # Frontend
   git clone https://github.com/mateuscarlos/cuidar_plus_api.git # Backend
   ```

2. **Acesse a pasta do backend:**
   ```bash
   cd cuidar_plus_api
   ```

3. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate # No Linux/Mac: source venv/bin/activate
   ```

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Inicie o servidor:**
   ```bash
   python app.py
   ```

6. **Acesse o backend no navegador:**
   ```
   http://127.0.0.1:5000
   ```

7. **Para interromper o servidor:**
   Pressione `CTRL+C` no terminal.

---

## Verificação das APIs

1. Após iniciar o servidor, acesse a documentação Swagger:
   ```
   http://127.0.0.1:5000/apidocs
   ```

2. Use o seguinte payload para testar a rota de cadastro de usuários:
   ```json
   {
     "cpf": "46161714752",
     "endereco": "Rua A, número 123 - Rio de Janeiro - RJ",
     "especialidade": "Estomaterapeuta",
     "funcao": "Enfermeiro Especialista",
     "nome": "Fernanda Oliveira",
     "registro_categoria": "123456",
     "setor": "operação"
   }
   ```

3. Após a primeira execução e instalação das dependências, basta seguir os passos:
   - Ativar o ambiente virtual.
   - Executar `python app.py`.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

