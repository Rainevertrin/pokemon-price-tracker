import gspread
import json
import os
from google.cloud import secretmanager
from google.oauth2 import service_account

def auth_gsheet():
    client = secretmanager.SecretManagerServiceClient()

    project_id = os.environ["PROJECT_ID"]
    secret_id = os.environ["SECRET_ID"]
    version_id = os.environ["VERSION_ID"]

    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(request={"name": secret_name})
    secret_payload = response.payload.data.decode("UTF-8")

    credentials_info = json.loads(secret_payload)
    creds = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=[
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ],
    )

    return gspread.authorize(creds)
