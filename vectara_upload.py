#adapted from https://docs.vectara.com/docs/getting-started-samples/rest_upload_file.py 

import os
import glob
import json
import logging
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
VECTARA_CUSTOMER_ID = os.getenv('VECTARA_CUSTOMER_ID')
VECTARA_CORPUS_ID = os.getenv('VECTARA_CORPUS_ID')
VECTARA_API_KEY = os.getenv('VECTARA_API_KEY')

def _get_upload_file_json(file_path):
    """Returns JSON file upload data."""
    with open(file_path, 'r') as file:
        text = file.read()

    document = {
        "document_id": os.path.basename(file_path),
        "title": os.path.basename(file_path),
        "metadata_json": json.dumps(
            {
                "file-name": os.path.basename(file_path),
                "directory": os.path.dirname(file_path),
            }
        ),
        "section": [
            {"text": text},
        ],
    }

    return json.dumps(document)

def upload_file(file_path, customer_id: int, corpus_id: int, idx_address: str, jwt_token: str):
    """Uploads a file to the corpus."""
    post_headers = {
        "Authorization": f"Bearer {jwt_token}"
    }
    response = requests.post(
        f"https://{idx_address}/v1/upload?c={customer_id}&o={corpus_id}",
        files={"file": (os.path.basename(file_path), _get_upload_file_json(file_path), "application/json")},
        verify=True,
        headers=post_headers)

    if response.status_code != 200:
        logging.error("REST upload failed with code %d, reason %s, text %s",
                       response.status_code,
                       response.reason,
                       response.text)
        return response, False

    message = response.json()["response"]
    if message["status"] and message["status"]["code"] not in ("OK", "ALREADY_EXISTS"):
        logging.error("REST upload failed with status: %s", message["status"])
        return message["status"], False

    return message, True

#Recursively get all HTML files in the 'Data' directory and its subdirectories
html_files = glob.glob('Data/**/*.html', recursive=True)

# Upload each HTML file
for file_path in html_files:
    upload_file(file_path, VECTARA_CUSTOMER_ID, VECTARA_CORPUS_ID, 'api.vectara.io', VECTARA_API_KEY)