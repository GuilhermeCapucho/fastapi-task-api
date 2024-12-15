## API RESTful de Gerenciamento de Tarefas

- Uma API construída com **FastAPI** que permite criar, atualizar, excluir e listar tarefas.
- Implementada autenticação JWT, níveis de acesso para usuários (admin e comum), e proteção de rotas.
- Banco de dados SQLite para armazenamento das informações.

---

- **Tecnologias Utilizadas**
    - **Linguagem**: Python 3.12
    - **Framework**: FastAPI
    - **Banco de Dados**: SQLite (com SQLAlchemy para ORM)
    - **Bibliotecas Importantes**:
        - `fastapi`
        - `sqlalchemy`
        - `pydantic`
        - `passlib` (para hashing de senhas)
        - `python-jose` (para JWT)
        - `uvicorn` (para rodar o servidor)



## Configuração do Ambiente

**Passos para configurar o projeto no ambiente local**:

1. Clone o repositório:
    
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd task-api
    ```
    
2. Crie um ambiente virtual:
    
    ```bash
    python -m venv venv
    ```
    
3. Ative o ambiente virtual:
    - **Windows**:
        
        ```bash
        venv\Scripts\activate
        ```
        
    - **Linux/MacOS**:
        
        ```bash
        source venv/bin/activate
        ```
        
4. Instale as dependências:
    
    ```bash
    pip install -r requirements.txt
    ```
    
5. Execute o banco de dados:
    
    ```bash
    python init_db.py
    ```
    
6. Inicie o servidor:
    
    ```bash
    uvicorn main:app --reload
    ```

## *Acesse a documentação gerada pelo FastAPI:*

- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc



## *Endpoints da API*

**1. Endpoints de Autenticação:**

- **Registro de Usuário (`/auth/register`)**:
    - Método: `POST`
    - Body:
        
        ```json
        {
          "username": "string",
          "password": "string",
          "email": "string",
          "is_admin": false
        }
        ```
        
    
    - Retorno:
        
        ```json
        {
          "message": "User registered successfully",
          "user": {
            "username": "string",
            "is_admin": false
        	}
        }
        ```
        

- **Login (`/auth/login`)**:
    - Método: `POST`
    - Body:
        
        ```json
        {
          "username": "string",
          "password": "string"
        }
        ```
        
    
    - Retorno:
        
        ```json
        {
          "access_token": "string",
          "token_type": "bearer"
        }
        ```
        

- **Logout (`/auth/logout`)**:
    - Método: `POST`
    - Header: Authorization: Bearer <TOKEN>
    - Retorno:
        
        ```json
        {
          "message": "Logout successful"
        }
        ```
        


**2. Endpoints de Tarefas:**

- **Obter todas as tarefas (`/api/tasks`)**:
    - Método: `GET`
    - Header: Authorization: Bearer <TOKEN>
    - Retorno:
        
        ```json
        {
          "tasks": [
            {
              "id": 1,
              "task": "string",
              "is_completed": false,
              "owner": "string"
            }
          ]
        }
        ```
        

- **Criar tarefa (`/api/tasks`)**:
    - Método: `POST`
    - Header: Authorization: Bearer <TOKEN>
    - Body:
        
        ```json
        {
          "task": "string",
          "is_completed": false
        }
        ```
        
    
    - Retorno:
        
        ```json
        {
          "message": "Task created successfully",
          "task": {
            "id": 1,
            "task": "string",
            "is_completed": false,
            "owner": "string"
          }
        }
        ```
        

- **Atualizar tarefa (`/api/tasks/{task_id}`)**:
    - Método: `PUT`
    - Header: Authorization: Bearer <TOKEN>
    - Body:
        
        ```json
        {
          "task": "string",
          "is_completed": true
        }
        ```
        
    
    - Retorno:
        
        ```json
        {
          "message": "Task updated successfully",
          "task": {
            "id": 1,
            "task": "string",
            "is_completed": true,
            "owner": "string"
          }
        }
        ```
        

- **Atualização Parcial (`/api/tasks/{task_id}`)**:
    - Método: `PATCH`
    - Header: Authorization: Bearer <TOKEN>
    - Body:
        
        ```json
        {
          "task": "string"
        }
        ```
        
    
    - Retorno:
        
        ```json
        {
          "message": "Task updated partially",
          "task": {
            "id": 1,
            "task": "string",
            "is_completed": true,
            "owner": "string"
          }
        }
        ```
        

- **Deletar tarefa (`/api/tasks/{task_id}`)**:
    - Método: `DELETE`
    - Header: Authorization: Bearer <TOKEN>
    - Retorno:


## Sugestões de melhorias futuras:

- Implementar paginação nos endpoints de tarefas.
- Adicionar filtros (ex: listar apenas tarefas concluídas ou pendentes).
- Melhorar autenticação com expiração de tokens ou refresh tokens.
- Testes automatizados com Pytest.
- Adicionar suporte para deploy (ex: Docker, Heroku ou AWS).
