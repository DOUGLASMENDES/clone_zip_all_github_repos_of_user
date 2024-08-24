import os
import subprocess
import requests
import zipfile

github_user = "<github username>"

def get_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error while trying to access repo: {response.status_code}")
        return []
    
def get_github_all_repos(username):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Error while accessing user repo: {response.status_code}")
            break
        
        page_repos = response.json()
        if not page_repos:
            # Exit loop when there are no more repos
            break
        
        repos.extend(page_repos)
        page += 1
    
    return repos

def clone_repos(repos, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    os.chdir(destination_folder)
    
    for repo in repos:
        clone_url = repo['clone_url']
        repo_name = repo['name']
        print(f"Cloning repo {repo_name}...")
        subprocess.run(["git", "clone", clone_url])

def zip_directories(directory):
    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)
        if os.path.isdir(folder_path) and folder_name != ".vs":
            zip_file_name = f"{folder_name}.zip"
            with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=folder_path)
                        zipf.write(file_path, arcname)
            print(f"Folder '{folder_name}' zipped to '{zip_file_name}'.")

def main():
    username = github_user 
    # Set the current folder as destiny
    destination_folder = os.path.dirname(os.path.abspath(__file__))
    
    repos = get_github_all_repos(username)
    if repos:
        clone_repos(repos, destination_folder)

        zip_directories(destination_folder)
    else:
        print("No repo found or error!")

if __name__ == "__main__":
    main()
