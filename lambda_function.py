import json
import base64
import requests
import os
import html
import re

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
REPO_OWNER = 'dfbr'
REPO_NAME = 'dfbr.github.io'
FILE_PATH = 'ordlist.csv'
BRANCH = 'main'

EXPECTED_TYPES = [
    "verb", "noun", "adjective", "phrase", "determiner",
    "conjunction", "subjunction", "preposition", "pronoun", "adverb"
]

NORWEGIAN_REGEX = re.compile(r'^[a-zA-ZåæøÅÆØ\s-]+$')
ENGLISH_REGEX = re.compile(r'^[a-zA-Z\s/\-\']+$')
IPV4_REGEX = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
IPV6_REGEX = re.compile(r'^[0-9a-fA-F:]+$')

def is_valid_ip(ip):
    return IPV4_REGEX.match(ip) or IPV6_REGEX.match(ip)

def get_client_ip(event):
    # Check for IP address in requestContext.http.sourceIp
    client_ip = event.get('requestContext', {}).get('http', {}).get('sourceIp')
    if client_ip and is_valid_ip(client_ip):
        return client_ip

    # Fallback to checking headers
    headers = event.get('headers', {})
    ip_headers = [
        'REMOTE_ADDR',
        'HTTP_X_FORWARDED_FOR',
        'HTTP_CLIENT_IP',
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED',
        'HTTP_X_CLUSTER_CLIENT_IP',
        'HTTP_FORWARDED_FOR',
        'HTTP_FORWARDED',
        'X_REAL_IP',
        'X-Real-IP',
        'x-real-ip'
    ]
    
    for header in ip_headers:
        if header in headers:
            ip = headers[header].split(',')[0].strip()
            if is_valid_ip(ip):
                return ip
    return 'unknown'

def lambda_handler(event, context):
    try:
        # Log the event object to understand its structure
        print("Received event:", json.dumps(event, indent=2))

        # Check if the body key exists in the event object
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps('Bad Request: Missing body in event')
            }

        # Parse the body
        body = json.loads(event['body'])

        # Validate type
        if 'type' not in body or body['type'] not in EXPECTED_TYPES:
            return {
                'statusCode': 400,
                'body': json.dumps('Bad Request: Invalid type')
            }

        # Validate word and translation
        if 'word' not in body or 'translation' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps('Bad Request: Missing word or translation')
            }

        # Validate Norwegian word
        word = body['word'].strip().lower()
        if not NORWEGIAN_REGEX.match(word):
            return {
                'statusCode': 400,
                'body': json.dumps('Bad Request: Invalid Norwegian word')
            }

        # Validate English translation
        translation = body['translation'].strip().lower()
        if not ENGLISH_REGEX.match(translation):
            return {
                'statusCode': 400,
                'body': json.dumps('Bad Request: Invalid English translation')
            }

        # Escape word and translation to be safe for saving to a file and displaying on a webpage
        word = html.escape(word)
        translation = html.escape(translation)

        # Validate gender
        if 'gender' not in body or body['gender'] not in ['m', 'n', 'fl', '']:
            return {
                'statusCode': 400,
                'body': json.dumps('Bad Request: Invalid gender')
            }

        gender = body['gender']

        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }

        # Get the current content of the CSV file from GitHub
        url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}'
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if 'content' not in response_data:
            print("Error fetching file from GitHub:", response_data)
            return {
                'statusCode': 500,
                'body': json.dumps('Error fetching file from GitHub')
            }

        current_data = base64.b64decode(response_data['content']).decode('utf-8')

        # Extract data from the event
        new_row = f"{body['type']},{word},{translation},{gender}\n"

        # Append the new row to the current data
        updated_data = current_data + new_row
        updated_data_encoded = base64.b64encode(updated_data.encode('utf-8')).decode('utf-8')

        # Get the client's IP address
        client_ip = get_client_ip(event)

        # Update the file on GitHub
        update_data = {
            'message': f'{client_ip} added {word}',
            'content': updated_data_encoded,
            'sha': response_data['sha'],
            'branch': BRANCH
        }

        update_response = requests.put(url, headers=headers, data=json.dumps(update_data))
        update_response_data = update_response.json()

        if update_response.status_code != 200:
            print("Error updating file on GitHub:", update_response_data)
            return {
                'statusCode': 500,
                'body': json.dumps('Error updating file on GitHub')
            }

        return {
            'statusCode': 200,
            'body': json.dumps('Word added successfully!')
        }

    except Exception as e:
        print("Exception:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal Server Error: {str(e)}')
        }