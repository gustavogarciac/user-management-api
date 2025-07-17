# API de Gerenciamento de Usuários

Uma API REST para gerenciamento de usuários construída com FastAPI, SQLite e arquitetura hexagonal. Este projeto demonstra práticas modernas de desenvolvimento Python com testes abrangentes e documentação completa.

## 🚀 Funcionalidades

- **Autenticação**: Sistema seguro de autenticação baseado em JWT
- **Gerenciamento de Usuários**: Operações CRUD completas para usuários
- **Paginação**: Paginação eficiente para listagens de usuários
- **Arquitetura Hexagonal**: Separação clara de responsabilidades com portas e adaptadores
- **Testes Abrangentes**: Testes unitários e de integração com relatórios de cobertura
- **Documentação da API**: Documentação Swagger/OpenAPI gerada automaticamente

## 🏗️ Arquitetura

Este projeto segue os princípios da **Arquitetura Hexagonal** (Portas e Adaptadores):

```
src/
├── domain/           # Lógica de negócio e entidades
│   ├── entities/     # Modelos de domínio (User, etc.)
│   ├── errors/       # Exceções específicas do domínio
│   └── ports/        # Definições de interfaces
├── application/      # Casos de uso e regras de negócio
│   └── use-cases/    # Serviços da aplicação
├── adapters/         # Interfaces externas
│   ├── api/          # Endpoints da API HTTP
│   ├── auth/         # Adaptadores de autenticação
│   └── repositories/ # Adaptadores de acesso a dados
├── infrastructure/   # Implementações técnicas
│   ├── config/       # Gerenciamento de configuração
│   └── database/     # Configuração e migrações do banco
└── main.py          # Ponto de entrada da aplicação
```

## 📁 Estrutura do Projeto

### Camada de Domínio (`src/domain/`)

- **Entities**: Objetos de negócio principais (User, etc.)
- **Errors**: Exceções específicas do domínio
- **Ports**: Definições de interfaces para dependências externas

### Camada de Aplicação (`src/application/`)

- **Use Cases**: Lógica de negócio e serviços da aplicação

### Camada de Adaptadores (`src/adapters/`)

- **API**: Endpoints HTTP e modelos de requisição/resposta
- **Auth**: Lógica de autenticação e autorização
- **Repositories**: Interfaces de acesso a dados

### Camada de Infraestrutura (`src/infrastructure/`)

- **Config**: Gerenciamento de configuração da aplicação
- **Database**: Configuração, migrações e gerenciamento de conexão do banco

## 📋 Requisitos

### Dependências de Produção

- **FastAPI**: Framework web moderno para construção de APIs
- **SQLAlchemy**: Kit de ferramentas SQL e ORM
- **Pydantic Settings**: Gerenciamento de configurações
- **Alembic**: Ferramenta de migração de banco de dados
- **Pwdlib**: Hash de senhas com Argon2
- **PyJWT**: Manipulação de tokens JWT
- **TZData**: Dados de fuso horário

### Dependências de Desenvolvimento

- **Ruff**: Linter e formatador Python rápido
- **Taskipy**: Executor de tarefas para fluxos de desenvolvimento

## 🛠️ Instalação

1. **Clone o repositório**

   ```bash
   git clone <url-do-repositório>
   cd user-management-api
   ```

2. **Crie o ambiente virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt # Caso você esteja em ambiente de desenvolvimento
   ```

4. **Configure as variáveis de ambiente**

   ```bash
   # Crie o arquivo .env com sua configuração
   cp .env.example .env
   ```

5. **Execute as migrações do banco**
   ```bash
   alembic upgrade head
   ```

## 🚀 Executando a Aplicação

### Servidor de Desenvolvimento

```bash
task run
# ou
fastapi dev src/main.py
```

### Servidor de Produção

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## 📚 Documentação da API

Após iniciar o servidor, acesse a documentação interativa da API:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testes

### Execute todos os testes

```bash
task test
```

### Execute testes com cobertura

```bash
task coverage
```

### Linting e formatação

```bash
task lint      # Verificar qualidade do código
task format    # Formatar código
```

## 🔧 Tarefas de Desenvolvimento

O projeto usa `taskipy` para tarefas comuns de desenvolvimento:

- `task lint`: Executar linting do código com Ruff
- `task format`: Formatar código com Ruff
- `task run`: Iniciar servidor de desenvolvimento
- `task test`: Executar testes com cobertura
- `task coverage`: Gerar relatório de cobertura

## 🔐 Recursos de Segurança

- **Autenticação JWT**: Autenticação segura baseada em tokens
- **Hash de Senhas**: Hash de senhas com Argon2 para segurança
- **Proteção de Rotas**: Endpoints protegidos com middleware de autenticação
- **Validação de Entrada**: Validação abrangente de requisições com Pydantic

## 📊 Banco de Dados

- **SQLite**: Banco de dados leve baseado em arquivo
- **SQLAlchemy ORM**: Mapeamento objeto-relacional
- **Migrações Alembic**: Versionamento de esquema do banco

## 🎯 Endpoints da API

### Autenticação

- `POST /auth/login` - Login do usuário
- `POST /auth/register` - Registro de usuário

### Usuários

- `GET /users` - Listar usuários (com paginação)
- `GET /users/{user_id}` - Obter usuário por ID
- `POST /users` - Criar novo usuário
- `PUT /users/{user_id}` - Atualizar usuário
- `DELETE /users/{user_id}` - Excluir usuário

## 📄 Licença

Este projeto faz parte de um teste prático para candidatura a vaga.

---

**Nota**: Esta é uma implementação de teste prático demonstrando práticas modernas de desenvolvimento Python com FastAPI e arquitetura hexagonal.
