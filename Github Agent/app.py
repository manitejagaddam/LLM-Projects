import os
import requests
import json
from dotenv import load_dotenv
from read_content import read_content

# Load environment variables from .env file
load_dotenv()

# Get GitHub username and token from environment variables
username = 'vetchayateesh'
token = os.getenv('GITHUB_TOKEN')  # Fetch token from the .env file

# Base URL for GitHub API
base_url = 'https://api.github.com'

# Function to get all repositories for a user
def get_repositories(username, token):
    repos = []
    url = f'{base_url}/user/repos'  # Fetch repositories for the authenticated user
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
    else:
        print(f"Failed to fetch repositories. Status code: {response.status_code}")
        print(f"Error message: {response.text}")
    return repos

# Function to recursively get files in a specific repository and subdirectories
def get_files_in_repo(owner, repo_name, token, path=''):
    files = {}
    url = f'{base_url}/repos/{owner}/{repo_name}/contents/{path}'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        for item in content:
            if item['type'] == 'file':  # If it's a file, add it to the current path
                files[item['name']] = item['path']
            elif item['type'] == 'dir':  # If it's a directory, recurse into it
                files[item['name']] = get_files_in_repo(owner, repo_name, token, item['path'])
    elif response.status_code == 403:
        print(f"Rate limit exceeded or unauthorized access in {repo_name}. Status code: {response.status_code}")
    else:
        print(f"Failed to fetch files in {repo_name}. Status code: {response.status_code}")
    return files

# Function to save the repository data to a JSON file
def save_repo_data_to_json(repositories_data, filename='repo_structure.json'):
    with open(filename, 'w') as json_file:
        json.dump(repositories_data, json_file, indent=4)

# Main function to fetch repositories, their files, and save them in JSON format
def main():
    # Define file paths to read
    file_paths = ["flickr/flickr/style.css", "flickr/flickr/index.html"]
    # file_paths = ["E-Comme..rce/README.md"]

    # Call the read_content function to read files
    content = read_content(username, "Web-Dev-Projects", file_paths)

    # Dictionary to hold repository file data
    repositories_data = {}

    # Fetch the list of repositories
    repositories = get_repositories(username, token)
    
    # Process each repository and fetch its files
    for repo in repositories:
        print(f"Processing repository: {repo['name']}")
        files = get_files_in_repo(username, repo['name'], token)
        repositories_data[repo['name']] = files

    # Save the collected data into a JSON file
    save_repo_data_to_json(repositories_data)

# Run the main function
if __name__ == "__main__":
    main()
