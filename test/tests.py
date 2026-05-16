import requests

# 1. Dados para o teste
create_user = {
    "name": "mia",
    "email": "mia@example.com",
    "password": "mia12345",
    "role": "user",
}

# 2. Definição dos Headers (Substitua pelo seu token real gerado no login)
user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwicm9sZSI6InVzZXIiLCJleHAiOjE3Nzg5NDk4MzZ9.arVopU2YLnpszjzOFdeuNORrw0w_C5n9z3s4zCcxBqg"
admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzc4OTQzNjcxfQ.rahmRVXEGxi3jdGfJVKXqhfB9ReQdLk0ZcA-hKji2FQ"

headers_autenticacao = {"Authorization": f"Bearer {user_token}"}

# 3. Requisição corrigida (URL limpa e parâmetro 'headers')
Requisicao_post = requests.post(
    "http://127.0.0.1:8000/v1/users", headers=headers_autenticacao, json=create_user
)

requisicao_get = requests.get(
    "http://127.0.0.1:8000/api/v1/auth/refresh_token",
    headers=headers_autenticacao,
)

if __name__ == "__main__":
    # 4. Print para você ver o resultado do teste no terminal
    print()
    print(f"Status Code: {requisicao_get.status_code}")
    print(f"Resposta: {requisicao_get.json()}")
    print()
