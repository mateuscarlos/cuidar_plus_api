# Prompt Padrão para Diretrizes de Desenvolvimento Backend

## Contexto do Projeto

- **Linguagem**: Python
- **Framework**: Flask
- **Banco de Dados**: MySQL
- **ORM**: SQLAlchemy
- **Padrão de Arquitetura**: Clean Architecture
- **Ferramentas de Teste**: Pytest
- **Outras Tecnologias**: Docker

## Regras e Padrões a Seguir

1. **Estrutura de Código**:
   - Seguir as convenções do PEP 8.
   - Organizar o código de acordo com o padrão Clean Architecture:
     - **Domain**: Regras de negócio e entidades.
     - **Application**: Casos de uso e lógica de aplicação.
     - **Infrastructure**: Integrações externas (banco de dados, APIs externas).
     - **Interface**: Endpoints e controladores.

2. **Endpoints**:
   - Utilizar FastAPI para criação de endpoints RESTful.
   - Seguir as convenções REST (ex.: verbos HTTP adequados: GET, POST, PUT, DELETE).
   - Implementar validação de dados com `pydantic` para requisições e respostas.
   - Adicionar documentação automática com OpenAPI (FastAPI gera automaticamente).

3. **Banco de Dados**:
   - Utilizar SQLAlchemy como ORM.
   - Criar migrations com Alembic.
   - Garantir que todas as queries sejam otimizadas para performance.
   - Usar transações para operações críticas.

4. **Segurança**:
   - Implementar autenticação e autorização (ex.: OAuth2 com JWT).
   - Sanitizar entradas do usuário para evitar injeções de SQL e outros ataques.
   - Configurar CORS adequadamente para endpoints públicos.

5. **Testes**:
   - Escrever testes unitários e de integração usando Pytest.
   - Garantir cobertura mínima de 80% para novos módulos.
   - Utilizar fixtures para simular banco de dados e dependências externas.

6. **Boas Práticas**:
   - Manter funções e métodos pequenos e com uma única responsabilidade.
   - Usar tipagem estática com `mypy` para melhorar a legibilidade e evitar erros.
   - Adicionar logs estruturados com `logging` para monitoramento e depuração.
   - Evitar duplicação de código (seguir o princípio DRY).

7. **Performance**:
   - Implementar cache com Redis para operações frequentes e dados estáticos.
   - Usar Celery para tarefas assíncronas e processamento em segundo plano.
   - Monitorar e otimizar consultas SQL para evitar gargalos.

8. **Docker e Deploy**:
   - Configurar o projeto para rodar em containers Docker.
   - Criar um `Dockerfile` otimizado e um `docker-compose.yml` para desenvolvimento local.
   - Garantir que as variáveis de ambiente sensíveis estejam protegidas (ex.: `.env`).

## Exemplo de Resposta Esperada

- Código gerado deve ser funcional e seguir as convenções acima.
- Incluir exemplos de validação de dados com `pydantic`.
- Garantir que o código seja modular e fácil de testar.

## Tecnologias e Padrões do Projeto Atual

- **Framework**: Flask
- **Banco de Dados**: MySql
- **ORM**: SQLAlchemy
- **Ferramentas de Teste**: Pytest
- **Outras Tecnologias**: Docker
