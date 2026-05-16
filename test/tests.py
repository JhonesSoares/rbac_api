import requests

# 1. Dados para o teste
create_user = {
    "name": "A",
    "email": "A@example.com",
    "password": "A1234567",
    "role": "user",
}

# 2. Definição dos Headers (Substitua pelo seu token real gerado no login)
user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwicm9sZSI6InVzZXIiLCJleHAiOjE3Nzg5NDk4MzZ9.arVopU2YLnpszjzOFdeuNORrw0w_C5n9z3s4zCcxBqg"
admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzc4OTY4NTk0fQ.yswWogmQEYGpGr5VsuZ9odF3XeRsNwQsQHp0R9hrRRs"

headers_autenticacao = {"Authorization": f"Bearer {admin_token}"}

# 3. Requisição corrigida (URL limpa e parâmetro 'headers')
requisicao_post = requests.post(
    "http://127.0.0.1:8000/api/v1/users", headers=headers_autenticacao, json=create_user
)

requisicao_get = requests.get(
    "http://127.0.0.1:8000/api/v1/auth/refresh_token",
    headers=headers_autenticacao,
)

if __name__ == "__main__":
    # 4. Print para você ver o resultado do teste no terminal
    print()
    print(f"Status Code: {requisicao_post.status_code}")
    print(f"Resposta: {requisicao_post.json()}")
    print()
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzc4OTY5MDc3fQ.n6Vs5_zt9oJdnlsX8ZE-hzcWBdzvrsZBEGHqmxUQt8M
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzc4OTY5OTcyfQ.cPxypC9EI5KNqSv0p8TkPYF3Yu2cZys82Jxo6OT5txI
