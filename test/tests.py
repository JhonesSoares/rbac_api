import requests

# 1. Dados para o teste
create_user = {
    "name": "lua",
    "email": "lua@example.com",
    "password": "lua12345",
    "role": "user",
}

# 2. Definição dos Headers (Substitua pelo seu token real gerado no login)
user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwicm9sZSI6InVzZXIiLCJleHAiOjE3NzkyMjgyNDZ9.3kwXNFP8RtXqnixH3Xw34ZjXEjhcuKcCfdYIxmxGO7U"
admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzc5MjI2OTU4fQ.HatQSRDao1tF9wA1wtlXRdCp0HaDFjTjpqv9K5esDPs"

headers_autenticacao = {"Authorization": f"Bearer {user_token}"}

# 3. Requisição corrigida (URL limpa e parâmetro 'headers')
requisicao_post = requests.post(
    "http://127.0.0.1:8000/api/v1/users", headers=headers_autenticacao, json=create_user
)

# requisicao_get = requests.get(
#    "http://127.0.0.1:8000/api/v1/auth/refresh_token",
#    headers=headers_autenticacao,
# )

my_data_get = requests.get(
    "http://127.0.0.1:8000/api/v1/users/list_users",
    headers=headers_autenticacao,
)

if __name__ == "__main__":
    # 4. Print para você ver o resultado do teste no terminal
    print()
    print(f"Status Code: {my_data_get.status_code}")
    print(f"Resposta: {my_data_get.json()}")
    print()
# 'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzc5MjIxMjgyfQ.jmSH_4DWsxHmJH4qJ9ikHD_v9ZbkKqccpKrRAX_OnDA'
