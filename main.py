import requests
import jwt
import os
from urllib.parse import urljoin
import argparse
from datetime import datetime, timedelta

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup command-line arguments parsing
parser = argparse.ArgumentParser(description='Fetch Youtube Video Summary and Transcript')
parser.add_argument('-i', '--id', type=str, help='Youtube Video ID', required=True)
args = parser.parse_args()

def main(video_id):
    base_url = os.getenv('BASE_URL')
    path = f"/summarize/{video_id}"
    complete_url = urljoin(base_url, path)

    token = jwt.encode(
        {
            "type": "youtube",
            "exp": datetime.utcnow() + timedelta(seconds=30)
        },
        os.getenv('JWT_SECRET'),
        algorithm="HS256"
    )

    headers = {'authorization': f'Bearer {token}'}
    response = requests.get(complete_url, headers=headers)
    return response.json()

if __name__ == '__main__':
    try:
        result = main(args.id)
        print('Summary:\n', result['summary'])
        print('\n')
        print('Transcript:\n', result['transcript'])
    except requests.exceptions.RequestException as e:
        print(e)
