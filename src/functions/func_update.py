import requests


def get_latest_release():
    """Получает данные о последнем релизе из GitHub API"""
    repo_name = "Nexon-Launcher"
    repo_owner = "Artyr717"

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        response = requests.get(url)
        response.raise_for_status()
        release_data = response.json()
        return release_data['tag_name'], release_data['html_url'], release_data['assets'][0]['browser_download_url']

    except Exception as e:
        print(f"Ошибка при обращении к GitHub API: {e}")
        return None, None, None
