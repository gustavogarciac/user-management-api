# Autenticação na API

Este documento explica como usar as dependências de autenticação implementadas na API.

## Dependências Disponíveis

### 1. `get_current_user` (Obrigatória)

Esta dependência **requer** que o usuário esteja autenticado. Se não houver token válido, retorna erro 401.

```python
from src.adapters.api.dependencies.auth import get_current_user

@router.get('/protected-route')
async def protected_endpoint(
    current_user: str = Depends(get_current_user)
):
    # current_user contém o email do usuário autenticado
    return {"message": f"Hello {current_user}!"}
```

### 2. `get_current_user_optional` (Opcional)

Esta dependência **não requer** autenticação. Se houver token válido, retorna o email do usuário; caso contrário, retorna `None`.

```python
from src.adapters.api.dependencies.auth import get_current_user_optional

@router.get('/public-route')
async def public_endpoint(
    current_user: Optional[str] = Depends(get_current_user_optional)
):
    if current_user:
        return {"message": f"Hello authenticated user {current_user}!"}
    else:
        return {"message": "Hello anonymous user!"}
```

## Como Usar

### 1. Importe a dependência

```python
from src.adapters.api.dependencies.auth import get_current_user
```

### 2. Adicione como parâmetro da função

```python
async def your_endpoint(
    # ... outros parâmetros ...
    current_user: str = Depends(get_current_user),
):
    # ... lógica da rota ...
```

### 3. Use o email do usuário autenticado

```python
async def your_endpoint(
    user_id: UUID,
    session: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user),
):
    # current_user contém o email do usuário autenticado
    # Você pode usar para verificar permissões, logs, etc.

    # Exemplo: verificar se o usuário está editando seu próprio perfil
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
```

## Rotas Protegidas

As seguintes rotas agora requerem autenticação:

- `GET /api/v1/users/{user_id}` - Buscar usuário específico
- `PUT /api/v1/users/{user_id}` - Atualizar usuário
- `DELETE /api/v1/users/{user_id}` - Deletar usuário
- `GET /api/v1/users/` - Listar usuários

## Rotas Públicas

As seguintes rotas não requerem autenticação:

- `POST /api/v1/auth/token` - Autenticar usuário
- `POST /api/v1/users/` - Criar novo usuário (registro)

## Exemplo de Uso Avançado

```python
from typing import Optional
from src.adapters.api.dependencies.auth import get_current_user_optional

@router.get('/analytics')
async def get_analytics(
    current_user: Optional[str] = Depends(get_current_user_optional)
):
    if current_user:
        # Usuário autenticado - retorna dados personalizados
        return {
            "user_email": current_user,
            "personalized_data": True,
            "analytics": {...}
        }
    else:
        # Usuário anônimo - retorna dados genéricos
        return {
            "user_email": None,
            "personalized_data": False,
            "analytics": {...}
        }
```

## Headers Necessários

Para usar rotas protegidas, inclua o header:

```
Authorization: Bearer <seu_jwt_token>
```

O token JWT pode ser obtido através da rota `POST /api/v1/auth/token`.
