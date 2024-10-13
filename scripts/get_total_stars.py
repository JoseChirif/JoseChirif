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
            response = requests.get(f"{url}?page={page}&per_page=100", timeout=10)  # 10 seconds timeout
            response.raise_for_status()  # Raise an exception for HTTP errors
            print(f"Fetching page {page}... Status code: {response.status_code}")
            data = response.json()

            if not data:
                break

            repositories.extend(data)
            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            break

    # Sum all the stars
    for repo in repositories:
        total_stars += repo['stargazers_count']

    return total_stars

if __name__ == "__main__":
    username = "JoseChirif"  # Replace with your GitHub username
    total_stars = get_total_stars(username)
    
    # Save the result in a JSON file in the same directory as the script
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Get the script directory
    json_file_path = os.path.join(script_directory, "stars_total.json")  # Create the full path for the JSON file
    
    with open(json_file_path, "w") as f:
        json.dump({"stars": total_stars}, f)

    print(f"Total stars: {total_stars}")
