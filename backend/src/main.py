import jwt
import time
from fastapi import FastAPI

#for making http requests
import requests 

APP_ID = "5903494"

with open("credentials/cloudagentproject.2026-11-24.private-key.pem", "r") as file:
    private_key = file.read()

payload = {
    "iat":int(time.time())-60,
    "exp":int(time.time())+600,
    "iss":APP_ID
}

jwt_token = jwt.encode(
    payload,
    private_key,
    algorithm="RS256"
)


app = FastAPI()
github_client_id = 'Iv23li5cjyZVKrMb3tr7'

headers = {
    "Authorization":f"Bearer {jwt_token}",
    "Accept":"application/vnd.github+json"
}

response = requests.get(
    "https://api.github.com/app/installations",
    headers=headers
)

installations = response.json()
installation_id = installations[0]["id"]

response = requests.post(
    f"https://api.github.com/app/installations/{installation_id}/access_tokens",
    headers=headers
)

# print("Token creation status:", response.status_code)

token_data = response.json()

token = response.json()["token"]

repo_response = requests.get(
    "https://api.github.com/installation/repositories",
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
)

# print(repo_response.status_code)
repositories = repo_response.json()['repositories']

for repo in repositories:
    print(repo["full_name"])

# for repo in repositories:
#     print(repo["full_name"])