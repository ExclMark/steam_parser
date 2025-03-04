import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_search_results(page: int = 1) -> dict:
    """
    Fetches search results from the Steam store.
    https://github.com/Revadike/InternalSteamWebAPI/wiki/Get-Search-Results

    Args:
        page (int): The page number of the search results to fetch. Defaults to 1.

    Returns:
        dict: A dictionary containing 25 search results in JSON format: 
        {"name": "game_name", "url": "game_url"}
    """
    url = "https://store.steampowered.com/search/results/"
    params = {
        "filter": "globaltopsellers",
        "category1": "998",  # Games
        "page": page,
        "json": 1
    }
    response = requests.get(url, params=params)
    return response.json()

def get_game_details(appid: int) -> dict:
    """
    Fetches details of a game from the Steam store.

    Args:
        appid (int): The Steam appid of the game.

    Returns:
        dict: A dictionary containing the details of the game in JSON format.
    """
    url = "https://store.steampowered.com/api/appdetails/"
    params = {
        "appids": appid
    }
    response = requests.get(url, params=params)
    return response.json()

def save_json(data: list, filename: str) -> None:
    """
    Saves a list of game details to a JSON file.

    Args:
        data (list): The list of game details to save.
        filename (str): The name of the file to save the dictionary to.
    """
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def extract_appid(logo_url: str) -> int:
    """
    Extracts the appid from the game logo URL.
    Note: This implementation assumes the URL has a fixed format.
    
    Args:
        logo_url (str): The URL containing the appid.
    
    Returns:
        int: The extracted appid.
    """
    try:
        # Remove the known prefix and split by '/' to get the appid
        prefix = "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/"
        appid_str = logo_url.replace(prefix, "").split('/')[0]
        return int(appid_str)
    except Exception as e:
        raise ValueError(f"Could not extract appid from logo URL '{logo_url}': {e}")

def main() -> None:
    games: list = []
    all_items: list = []

    pages: int = 2  # Number of pages to fetch
    save_dir: str = "search_results.json" # File to save the search results

    print(f"Retrieving {25 * pages} games from the Steam store...", end=' ', flush=True)
    # Fetch search results concurrently for each page
    with ThreadPoolExecutor(max_workers=pages) as executor:
        future_to_page: dict = {
            executor.submit(get_search_results, page): page for page in range(1, pages + 1)
        }
        for future in as_completed(future_to_page):
            page_data: dict = future.result()
            all_items.extend(page_data.get("items", []))
    print("[OK]")

    # Fetch game details concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_name: dict = {}
        for game in all_items:
            game_name: str = game.get("name", "Unknown Game")
            logo_url: str = game.get("logo", "")
            try:
                app_id: int = extract_appid(logo_url)
            except ValueError as e:
                print(f"Skipping {game_name}: {e}")
                continue
            future = executor.submit(get_game_details, app_id)
            future_to_name[future] = game_name

        for future in as_completed(future_to_name):
            game_name: str = future_to_name[future]
            try:
                details: dict = future.result()
                games.append(details)
                print(f"Fetched {game_name}... [OK]")
            except Exception as exc:
                print(f"Error fetching details for {game_name}: {exc}")

    save_json(games, save_dir)
    print(f'All game details saved to {save_dir}.')

if __name__ == '__main__':
    main()
