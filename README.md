# CUIDAR+ API

## Visão Geral

Bem-vindo à API do **CUIDAR+**, a espinha dorsal do nosso sistema de assistência à saúde. Esta API foi projetada para facilitar a gestão de cuidados médicos, conectando pacientes, cuidadores e profissionais de saúde em uma plataforma integrada e intuitiva.

## 🚀 Funcionalidades Principais

- **Gestão de Pacientes**: Cadastro completo de informações médicas, histórico e necessidades de cuidados
- **Agendamento de Cuidados**: Sistema avançado para organização de visitas e tratamentos
- **Monitoramento em Tempo Real**: Acompanhamento de métricas de saúde e atividades diárias
- **Notificações Inteligentes**: Alertas para medicações, consultas e alterações no quadro de saúde
- **Relatórios Analíticos**: Geração de insights baseados em dados coletados

## 🛠️ Tecnologias Utilizadas

- **Python/Flask**: Framework web para desenvolvimento da API
- **SQLAlchemy**: ORM para interação com o banco de dados
- **MySQL**: Sistema de gerenciamento de banco de dados
- **Alembic**: Ferramenta para migrações de banco de dados
- **Docker**: Containerização para implantação simplificada
- **JWT**: Autenticação segura de usuários
- **Pytest**: Framework para testes automatizados

## 📋 Pré-requisitos

- Docker e Docker Compose
- Python 3.8+
- MySQL 8.0+

## ⚙️ Configuração e Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/mateuscarlos/cuidar-plus-api.git
   cd cuidar_plus_api
   ```

2. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto com as configurações necessárias:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=sua-chave-secreta
   DATABASE_URL=mysql+pymysql://usuario:senha@db:3306/cuidar_plus_bd
   ```

3. **Inicie os contêineres Docker:**
   ```bash
   docker-compose -f docker-compose.db.yml -f docker-compose.backend.yml up -d
   ```

4. **Execute as migrações do banco de dados:**
   ```bash
   docker-compose exec backend flask db upgrade
   ```

## 🔌 Endpoints da API

### Pacientes
- `GET /api/exibe_pacientes`: Lista todos os pacientes
- `GET /api/exibe_paciente/<id>`: Obtém detalhes de um paciente específico
- `GET /api/buscar_paciente`: Busca pacientes com filtros (nome, CPF, ID)
- `POST /api/criar_paciente`: Cria um novo paciente
- `PUT /api/atualiza_paciente/<id>`: Atualiza dados de um paciente
- `DELETE /api/excluir_paciente/<id>`: Remove um paciente

### Acompanhamentos
- `GET /pacientes/<id>/acompanhamentos`: Lista acompanhamentos de um paciente
- `GET /acompanhamentos/<id>`: Obtém detalhes de um acompanhamento específico
- `POST /acompanhamentos`: Registra um novo acompanhamento
- `PUT /acompanhamentos/<id>`: Atualiza um acompanhamento existente

### Usuários
- `POST /users`: Cria um novo usuário
- `GET /users`: Lista todos os usuários
- `GET /users/<id>`: Obtém detalhes de um usuário específico
- `PUT /users/<id>`: Atualiza informações de usuário
- `DELETE /users/<id>`: Remove um usuário

### Convênios e Planos
- `POST /convenios`: Cria um novo convênio
- `GET /convenios`: Lista todos os convênios disponíveis

## 🧪 Testes

Para executar a suíte de testes:

```bash
docker-compose exec backend pytest
```

Para verificar a cobertura dos testes:

```bash
docker-compose exec backend pytest --cov=app tests/
```

## 🔒 Segurança

A API implementa diversas medidas de segurança:
- Autenticação via JWT (JSON Web Tokens)
- Validação de CPF para cadastro de pacientes
- Sanitização de inputs para prevenir injeções SQL
- Configuração de CORS para controlar domínios com acesso permitido
- Proteção contra requisições duplicadas

## 📦 Monitoramento e Manutenção

### Verificar logs da aplicação:
```bash
docker-compose logs -f backend
```

### Reiniciar serviços:
```bash
docker-compose restart backend
```

### Verificar status dos contêineres:
```bash
docker-compose ps
```

## 🤝 Contribuindo

1. Faça um fork do repositório
2. Crie um branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para o branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Modelo de Dados

### Paciente
- Dados pessoais: nome, CPF, data de nascimento, gênero
- Informações médicas: CID primário/secundário, alergias
- Contatos: telefone, email, contato de emergência
- Endereço: rua, número, complemento, bairro, cidade, estado
- Convênio: ID do convênio, ID do plano, número da carteirinha

### Acompanhamento
- Dados do atendimento: data, hora, tipo
- Sinais vitais: pressão arterial, temperatura, etc.
- Avaliações: dispositivos, intervenções, plano de ação

### Usuário
- Dados pessoais: nome, email, cargo
- Credenciais: hash da senha, permissões
- Informações profissionais: especialidade, registro, setor

## 📞 Suporte

Em caso de dúvidas ou problemas, entre em contato conosco:
- Email: suporte@cuidarmais.com
- Issue Tracker: https://github.com/seu-usuario/cuidar-plus-api/issues

---
