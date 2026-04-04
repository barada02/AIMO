import requests
from bs4 import BeautifulSoup
import json
import time
import os

OUTPUT_FILE = "aime_dataset.json"

def get_soup(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return BeautifulSoup(response.text, 'html.parser')

def scrape_problem_page(url):
    soup = get_soup(url)
    if not soup:
        return None
    
    content = soup.find('div', {'id': 'mw-content-text'})
    if not content:
        return None
        
    return content.text.strip()

def main():
    dataset = []
    
    # Example: you can adjust the range of years here
    for year in range(2023, 2024):  # Testing with 2023 only for now
        sets = ['I', 'II'] if year >= 2000 else ['']
            
        for s in sets:
            set_name = s if s else 'AIME'
            print(f"Scraping {year} {set_name}")
            
            for i in range(1, 16):
                if s:
                    title = f"{year}_AIME_{s}_Problems/Problem_{i}"
                else:
                    title = f"{year}_AIME_Problems/Problem_{i}"
                    
                url = f"https://artofproblemsolving.com/wiki/index.php?title={title}"
                print(f"  Fetching {title}...")
                
                text = scrape_problem_page(url)
                if text:
                    # Basic parsing to store raw text. You can add regex passing here later
                    dataset.append({
                        'year': year,
                        'set': set_name,
                        'problem_number': i,
                        'url': url,
                        'raw_text': text
                    })
                time.sleep(1)  # Be nice to the server

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()