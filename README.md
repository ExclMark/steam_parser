# 🚀 Steam games parser

A fast and threaded parser for fetching top-selling games from the Steam API.

## 📦 Setup & Installation

1. **Clone the repo:**
   ```sh
   git clone https://github.com/ExclMark/steam_parser.git
   cd steam_parser
   ```

2. **Create a virtual environment (optional but recommended):**
   ```sh
   python3 -m venv env
   source env/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## ⚡ Usage

Run the script to fetch 50 top-selling games and save them as JSON:
```sh
python main.py
```

The results will be saved in `search_results.json`.

### Customization
Edit line 78 in `main.py` to change the number of games to fetch. <br>
1 page has 25 games from the search results.
```python
pages: int = 2  # Number of pages to fetch
```


## 🛠 Requirements
- Python 3.8+
- `requests` library

