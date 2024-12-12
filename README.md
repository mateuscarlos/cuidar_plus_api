# Cuidar_plus_api
## Apis da Aplicação Cuidar +

### Como executar a aplicação:
- Crie uma pasta local para que os 2 repositórios possam ser armazenados;
- Clone os repositórios e coloque os dois na mesma pasta;
- Abra o terminal no Visual Studio Code
- Navegue para a Pasta cuidar_plus_api com o comando cd cuidar_plus_api;
- Rode o comando python -m venv venv para criar o ambiente de desenvolvimento virtual;
- Em seguida rode o comando venv\Scripts\activate para ativar o ambiente de desenvolvimento virtual;
- Execute o comando pip install -r requirements.txt para instalação das dependências da aplicação;
- Execute o comando python app.py para inicialização do servidor da aplicação;
- Abra o navegador e acesse http://127.0.0.1:5000 para iniciar a aplicação.

### Verificação das APIs via Swagger
Após a inicialização do servidor siga o caminho http://127.0.0.1:5000/apidocs para abrir o swagger;
Dados fictícios para serem usados para teste da roda de cadastro de usuários:
```{ "cpf": "46161714752", "endereco": "Rua A, número 123 - Rio de Janeiro - RJ", "especialidade": "Estomaterapeuta", "funcao": "Enermeiro Especialista", "nome": "Fernanda Oliveira", "registro_categoria": "123456", "setor": "operacao" }```
