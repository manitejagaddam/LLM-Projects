import requests
import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# GitHub username and token
username = 'vetchayateesh'
token = os.getenv('GITHUB_TOKEN')  # Fetch token from environment variable

base_url = 'https://api.github.com'

# Function to get raw file content from a specific repository
def get_file_content(owner, repo_name, file_path):
    url = f'{base_url}/repos/{owner}/{repo_name}/contents/{file_path}'
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_content = response.json()
        return file_content['content']
    else:
        print(f"Failed to fetch file content from {file_path}. Status code: {response.status_code}")
        return None

# Function to read content of multiple files
def read_content(username, repo_name, file_paths):
    content = {}
    
    
    for file_path in file_paths:
        content = get_file_content(username, repo_name, file_path)
        if content:
            # GitHub API returns file content encoded in base64, decode it
            decoded_content = base64.b64decode(content).decode('utf-8')
            print(f"Content of {file_path}:\n{decoded_content}")
            
            content[file_path.split("/")[-1]] = decoded_content
    
    return content
