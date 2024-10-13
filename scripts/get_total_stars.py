import requests
import json
import os

def get_total_stars(username):
    url = f"https://api.github.com/users/{username}/repos"
    repositories = []
    page = 1
    total_stars = 0

    while True:
        try:
            response = requests.get(f"{url}?page={page}&per_page=100", timeout=10)  # 10 seconds wait
            response.raise_for_status()  # Raises an HTTP error for bad responses
            print(f"Fetching page {page}... Status code: {response.status_code}")
            data = response.json()

            if not data:
                break

            repositories.extend(data)
            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            break

    # Sum all stars
    for repo in repositories:
        total_stars += repo['stargazers_count']

    return total_stars

if __name__ == "__main__":
    username = "JoseChirif"  # Replace with your GitHub username
    total_stars = get_total_stars(username)

    # Save the result in a JSON file for shields.io
    json_data = {
        "schemaVersion": 1,
        "label": "stars",
        "message": str(total_stars),  # Convert the star count to string
        "color": "yellow"  # You can change this color as needed
    }

    json_file_path = os.path.join(os.path.dirname(__file__), "stars_total.json")
    with open(json_file_path, "w") as f:
        json.dump(json_data, f)

    print(f"Total stars: {total_stars}")
