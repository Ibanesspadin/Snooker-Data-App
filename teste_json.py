from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file(
    "config/credentials.json"
)

print("JSON carregado com sucesso!")
