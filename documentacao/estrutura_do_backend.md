# Estrutura de Diretórios Recomendada

cuidar_plus_api/
├── src/                         # Código fonte principal
│   ├── domain/                  # Camada de domínio (regras de negócio centrais)
│   │   ├── entities/            # Entidades de negócio
│   │   │   ├── user.py          # Entidade de usuário
│   │   │   └── patient.py       # Entidade de paciente (já existente)
│   │   ├── repositories/        # Interfaces dos repositórios (abstrações)
│   │   │   ├── user_repository.py
│   │   │   └── patient_repository.py
│   │   ├── services/            # Serviços de domínio puros
│   │   │   ├── user_service.py
│   │   │   └── patient_service.py
│   │   └── exceptions/          # Exceções específicas de domínio
│   │       └── domain_exceptions.py
│   │
│   ├── application/             # Camada de aplicação (casos de uso)
│   │   ├── dtos/                # Data Transfer Objects
│   │   │   ├── user_dto.py
│   │   │   └── patient_dto.py
│   │   ├── interfaces/          # Interfaces da camada de aplicação
│   │   │   └── services/        # Interfaces dos serviços de aplicação
│   │   │       ├── auth_service_interface.py
│   │   │       └── user_service_interface.py
│   │   └── services/            # Implementações dos casos de uso
│   │       ├── auth_service.py  # Lida com autenticação
│   │       └── user_service.py  # Implementação dos casos de uso de usuário
│   │
│   ├── infrastructure/          # Camada de infraestrutura
│   │   ├── database/            # Implementações relacionadas ao banco de dados
│   │   │   ├── config.py        # Configuração da conexão
│   │   │   ├── models/          # Modelos ORM
│   │   │   │   ├── user.py
│   │   │   │   └── patient.py
│   │   │   └── repositories/    # Implementações concretas dos repositórios
│   │   │       ├── user_repository.py
│   │   │       └── patient_repository.py
│   │   ├── security/            # Componentes de segurança
│   │   │   ├── password_service.py  # Serviço para manipulação de senhas
│   │   │   └── token_service.py     # Serviço para JWT tokens
│   │   ├── logging/             # Serviços de log
│   │   │   └── logger.py
│   │   └── external/            # Serviços externos (se houver)
│   │
│   ├── interfaces/              # Adaptadores de interface
│   │   ├── api/                 # API REST
│   │   │   ├── controllers/     # Controladores da API
│   │   │   │   ├── user_controller.py
│   │   │   │   └── patient_controller.py
│   │   │   ├── middlewares/     # Middlewares
│   │   │   │   ├── auth_middleware.py
│   │   │   │   └── error_handler.py
│   │   │   ├── schemas/         # Esquemas de validação para a API
│   │   │   │   ├── user_schema.py
│   │   │   │   └── patient_schema.py
│   │   │   ├── routes/          # Definição de rotas
│   │   │   │   ├── auth_routes.py
│   │   │   │   ├── user_routes.py
│   │   │   │   └── patient_routes.py
│   │   │   └── app.py          # Configuração da aplicação API
│   │   └── cli/                # Interface de linha de comando
│   │       └── admin_commands.py  # Comandos administrativos
│   │
│   └── config/                 # Configurações globais
│       ├── settings.py         # Configurações da aplicação
│       └── container.py        # Container de injeção de dependências
│
├── tests/                      # Testes automatizados
│   ├── unit/                   # Testes unitários
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/            # Testes de integração
│   └── fixtures/               # Fixtures para testes
│
├── scripts/                    # Scripts utilitários
│   ├── create_root_user.py     # Script para criar usuário root
│   └── db_migrations.py        # Scripts para migrações
│
├── migrations/                 # Migrações de banco de dados
│   └── versions/
│
├── docs/                       # Documentação
│   └── api/                    # Documentação da API
│
├── .env.example                # Template de variáveis de ambiente
├── requirements.txt            # Dependências do projeto
├── Dockerfile                  # Configuração do Docker
└── docker-compose.yml          # Configuração do Docker Compose

## Principais Modificações e Justificativas

1. **Estrutura src**:
   - Adicionada para isolar todo o código fonte em um único diretório
   - Facilita a organização e localização de componentes

2. **Separação mais clara entre interfaces e implementações**:
   - Repositórios definidos como interfaces na camada de domínio
   - Implementações concretas na camada de infraestrutura
   - Respeita o Princípio de Inversão de Dependência (SOLID)

3. **Controladores separados de rotas**:
   - Controladores contêm a lógica de tratamento de requisições
   - Rotas apenas definem os endpoints e chamam os controladores
   - Melhora a Responsabilidade Única (SOLID)

4. **Container de injeção de dependências**:
   - Facilita a implementação do Princípio de Inversão de Dependência
   - Melhora a testabilidade do código

5. **Estrutura de testes espelhando a arquitetura**:
   - Testes organizados por camada da arquitetura
   - Testes de integração e unitários separados

6. **Diretório de scripts**:
   - Scripts utilitários separados do código principal
   - Ferramentas administrativas como criação de usuário root

## Arquivos a Criar ou Modificar

1. **Arquivos Fundamentais**:
   - `src/domain/entities/user.py` - Definição da entidade de usuário
   - `src/domain/repositories/user_repository.py` - Interface do repositório
   - `src/application/services/auth_service.py` - Serviço de autenticação
   - `src/infrastructure/security/token_service.py` - Geração e validação de JWT
   - `src/interfaces/api/routes/auth_routes.py` - Rota de login
   - `src/config/container.py` - Container de injeção de dependências

2. **Arquivos de Configuração**:
   - `src/config/settings.py` - Substituir/expandir o config.py existente
   - `.env.example` - Template de variáveis de ambiente
   - Dockerfile e docker-compose.yml - Atualizar para a nova estrutura

Esta estrutura mantém os princípios SOLID e Clean Architecture, separando claramente as responsabilidades e garantindo que as dependências fluam de fora para dentro (domínio no centro).

A parte de pacientes, como solicitado, permanecerá inalterada em termos de funcionalidade, mas sua estrutura será ajustada para se alinhar com a nova organização.