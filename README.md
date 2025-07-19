# User Management API

API REST para gerenciamento de usuários construída com **FastAPI**, **SQLite**, e seguindo a **arquitetura hexagonal (ports and adapters)**. Este projeto demonstra práticas modernas de desenvolvimento Python, incluindo autenticação segura com JWT, operações CRUD completas com paginação avançada, testes abrangentes (unitários e de integração), e documentação automática via Swagger/OpenAPI.

## 🚀 Funcionalidades

- **🔐 Autenticação Segura**: Sistema de login com tokens JWT e proteção de rotas
- **👥 Gerenciamento de Usuários**: CRUD completo (Create, Read, Update, Delete) com validação robusta
- **📄 Paginação Avançada**: Listagem com paginação, filtros, ordenação e busca textual
- **🏗️ Arquitetura Hexagonal**: Separação clara de responsabilidades com portas, adaptadores e casos de uso
- **🧪 Testes Abrangentes**: Cobertura completa com testes unitários e de integração
- **📚 Documentação Interativa**: Swagger/OpenAPI gerada automaticamente
- **🐳 Containerização**: Suporte a Docker para desenvolvimento e produção
- **🔧 Qualidade de Código**: Linting, formatação e relatórios de cobertura

## 🏗️ Arquitetura Hexagonal

O projeto adota a **arquitetura hexagonal** para garantir modularidade, testabilidade e manutenibilidade:

```
src/
├── domain/                    # 🎯 Lógica de negócio e entidades
│   ├── entities/             # Modelos de domínio (User)
│   ├── errors/               # Exceções específicas do domínio
│   └── ports/                # Definições de interfaces (contratos)
├── application/              # 🚀 Casos de uso e regras de negócio
│   └── use_cases/           # Serviços da aplicação
├── adapters/                 # 🔌 Interfaces externas
│   ├── api/                 # Endpoints da API HTTP
│   │   ├── dependencies/    # Injeção de dependências
│   │   ├── routers/        # Rotas da API
│   │   └── schemas/        # Modelos de requisição/resposta
│   ├── auth/               # Adaptadores de autenticação
│   └── repositories/       # Adaptadores de acesso a dados
├── infrastructure/          # ⚙️ Implementações técnicas
│   ├── config/            # Gerenciamento de configuração
│   └── database/          # Configuração e migrações do banco
└── factories/              # 🏭 Fábricas para injeção de dependências
```

### Princípios da Arquitetura

- **Inversão de Dependência**: O domínio não depende de implementações externas
- **Separação de Responsabilidades**: Cada camada tem uma responsabilidade específica
- **Testabilidade**: Fácil mock e teste de cada componente isoladamente
- **Flexibilidade**: Troca de implementações sem afetar a lógica de negócio

## 📋 Requisitos

### Dependências de Produção

- **Python 3.10+**: Linguagem base do projeto
- **FastAPI**: Framework web moderno para construção de APIs
- **SQLAlchemy**: ORM para acesso ao banco de dados
- **Alembic**: Ferramenta de migração de banco de dados
- **Pwdlib**: Hash de senhas com Argon2 (segurança)
- **PyJWT**: Manipulação de tokens JWT
- **Pydantic**: Validação de dados e serialização

### Dependências de Desenvolvimento

- **Ruff**: Linter e formatador Python rápido
- **Taskipy**: Executor de tarefas para fluxos de desenvolvimento
- **Pytest**: Framework de testes
- **Pytest-cov**: Relatórios de cobertura de código
- **HTTPX**: Cliente HTTP para testes de integração

## 🛠️ Instalação e Configuração

### 1. Clone o Repositório

```bash
git clone <url-do-repositório>
cd user-management-api
```

### 2. Crie o Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
# Dependências de produção
pip install -r requirements.txt

# Dependências de desenvolvimento
pip install -r requirements-dev.txt
```

### 4. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite+aiosqlite:///./data/users.db
JWT_SECRET_KEY=sua_chave_secreta_muito_segura_aqui
JWT_EXPIRATION_MINUTES=30
```

### 5. Execute as Migrações do Banco

```bash
# Inicialize o Alembic (primeira vez)
alembic init src/infrastructure/database/migrations

# Execute as migrações
alembic upgrade head
```

## 🚀 Executando a Aplicação

### Desenvolvimento Local

```bash
# Usando taskipy (recomendado)
task run

# Ou diretamente com FastAPI
fastapi dev src/main.py

# Ou com uvicorn
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Com Docker

```bash
# Construa a imagem
docker build -t user-management-api .

# Execute o container
docker run -p 8000:8000 user-management-api

# Ou use docker-compose
docker-compose up --build
```

### Produção

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## 📚 Documentação da API

Após iniciar o servidor, acesse a documentação interativa:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Autenticação

### 1. Obter Token de Acesso

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=seu_email@exemplo.com&password=sua_senha"
```

### 2. Usar Token nas Requisições

```bash
curl -X GET "http://localhost:8000/api/v1/users" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 🎯 Endpoints da API

### Autenticação

| Método | Endpoint             | Descrição                     |
| ------ | -------------------- | ----------------------------- |
| `POST` | `/api/v1/auth/token` | Login e obtenção de token JWT |

### Usuários

| Método   | Endpoint                  | Descrição                                 |
| -------- | ------------------------- | ----------------------------------------- |
| `GET`    | `/api/v1/users`           | Listar usuários (com paginação e filtros) |
| `GET`    | `/api/v1/users/{user_id}` | Obter usuário por ID                      |
| `POST`   | `/api/v1/users`           | Criar novo usuário                        |
| `PUT`    | `/api/v1/users/{user_id}` | Atualizar usuário                         |
| `DELETE` | `/api/v1/users/{user_id}` | Excluir usuário                           |

### Parâmetros de Paginação e Filtros

A listagem de usuários suporta:

- **Paginação**: `page` e `page_size`
- **Busca**: `query` (busca em username e email)
- **Filtros**: `username` e `email`
- **Ordenação**: `order_by` e `order_direction`

**Exemplo de uso:**

```
GET /api/v1/users?page=1&page_size=10&query=john&order_by=created_at&order_direction=desc
```

## 🧪 Testes

### Executar Todos os Testes

```bash
# Com taskipy (recomendado)
task test

# Ou diretamente
pytest -s -x --cov=src -vv
```

### Executar Testes Específicos

```bash
# Apenas testes unitários
pytest tests/unit/

# Apenas testes de integração
pytest tests/integration/

# Teste específico
pytest tests/unit/test_create_user_use_case.py
```

### Relatório de Cobertura

```bash
# Gerar relatório HTML
task coverage

# O relatório estará disponível em htmlcov/index.html
```

### Qualidade de Código

```bash
# Linting
task lint

# Formatação automática
task format

# Verificar e corrigir problemas
task pre_format
```

## 🔧 Tarefas de Desenvolvimento

O projeto usa `taskipy` para automatizar tarefas comuns:

| Comando           | Descrição                                    |
| ----------------- | -------------------------------------------- |
| `task lint`       | Executar linting do código com Ruff          |
| `task format`     | Formatar código com Ruff                     |
| `task pre_format` | Verificar e corrigir problemas de formatação |
| `task run`        | Iniciar servidor de desenvolvimento          |
| `task test`       | Executar testes com cobertura                |
| `task coverage`   | Gerar relatório de cobertura HTML            |
| `task pre_test`   | Executar linting antes dos testes            |

## 🔐 Recursos de Segurança

- **Autenticação JWT**: Tokens seguros com expiração configurável
- **Hash de Senhas**: Argon2 para hash seguro de senhas
- **Proteção de Rotas**: Middleware de autenticação em endpoints protegidos
- **Validação de Entrada**: Validação robusta com Pydantic
- **Tratamento de Erros**: Exceções específicas do domínio

## 📊 Banco de Dados

- **SQLite**: Banco de dados leve e portável
- **SQLAlchemy ORM**: Mapeamento objeto-relacional assíncrono
- **Migrações Alembic**: Versionamento de esquema do banco
- **Transações**: Suporte a transações ACID

## 🏗️ Estrutura de Testes

### Testes Unitários (`tests/unit/`)

- **Casos de Uso**: Testes isolados para cada caso de uso
- **Serviços**: Testes para serviços de autenticação e hash
- **Repositórios**: Testes para interfaces de acesso a dados

### Testes de Integração (`tests/integration/`)

- **Rotas da API**: Testes end-to-end dos endpoints
- **Banco de Dados**: Testes de integração com SQLite
- **Repositórios**: Testes de implementação concreta

### Cobertura de Testes

O projeto mantém alta cobertura de testes, incluindo:

- Casos de sucesso e erro
- Validações de entrada
- Tratamento de exceções
- Cenários edge cases

## 🐳 Docker

### Desenvolvimento

```bash
# Construir imagem
docker build -t user-management-api:dev .

# Executar com volumes para desenvolvimento
docker run -p 8000:8000 -v $(pwd)/src:/app/src user-management-api:dev
```

### Produção

```bash
# Usar docker-compose
docker-compose up --build

# Ou executar diretamente
docker run -p 8000:8000 user-management-api
```

## 📈 Monitoramento

- **Health Check**: Endpoint `/health` para verificação de status
- **Logs**: Logs estruturados para debugging
- **Métricas**: Endpoints para monitoramento de performance

---

**Nota**: Esta implementação demonstra práticas modernas de desenvolvimento Python, incluindo arquitetura hexagonal, testes abrangentes, segurança robusta e documentação completa. O projeto está pronto para produção e pode ser facilmente estendido com novas funcionalidades.
