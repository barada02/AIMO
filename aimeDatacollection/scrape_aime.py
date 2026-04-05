import requests
from bs4 import BeautifulSoup
import json
import time
import os
import sys

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
    
    content = soup.find('div', {'class': 'mw-parser-output'})
    if not content:
        content = soup.find('div', {'id': 'mw-content-text'})
    if not content:
        return None
        
    # Remove table of contents
    toc = content.find('div', {'id': 'toc'})
    if toc:
        toc.decompose()
        
    # Extract math from MathJax/LaTeX image tags before calling .text
    for img in content.find_all('img', class_='latex'):
        if img.has_attr('alt'):
            img.replace_with(img['alt'])
            
    parsed_data = {}
    current_section = "Intro"
    section_content = []
    
    for elem in content.children:
        # Only split sections on h1 and h2 (major headers like "Problem" and "Solution 1")
        if getattr(elem, 'name', None) in ['h1', 'h2']:
            # Save previous section
            text = '\n'.join([p.text.strip() for p in section_content if getattr(p, 'text', '').strip()])
            if text:
                parsed_data[current_section] = text
            
            # Start new section
            current_section = elem.text.replace('[edit]', '').strip()
            section_content = []
        elif getattr(elem, 'name', None) is not None:
            # h3, h4, p, ul, ol etc all get added to the current section
            section_content.append(elem)
            
    # Save the last section
    text = '\n'.join([p.text.strip() for p in section_content if getattr(p, 'text', '').strip()])
    if text:
        parsed_data[current_section] = text
        
    formatted_data = {
        'problem': '',
        'other': {}
    }
    
    sol_counter = 1
    for key, val in parsed_data.items():
        k_lower = key.lower()
        if 'problem' in k_lower and not formatted_data['problem']:
            formatted_data['problem'] = val
        elif 'solution' in k_lower and 'video' not in k_lower and 'see also' not in k_lower:
            formatted_data[f'solution{sol_counter}'] = val
            sol_counter += 1
        elif k_lower == 'intro' and not val:
            continue
        else:
            formatted_data['other'][key] = val
            
    return formatted_data

def main():
    mode = "test"
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
    dataset = []
    
    if mode == "test":
        print("Running in TEST mode (1 year, 1 set, 2 problems)")
        years = range(2026, 2027)
        get_sets = lambda y: ['I']
        problem_range = range(1, 3)
    elif mode == "full":
        print("Running in FULL mode (1983-2026, all sets, 15 problems)")
        years = range(1983, 2027)
        get_sets = lambda y: ['I', 'II'] if y >= 2000 else ['']
        problem_range = range(1, 16)
    else:
        print(f"Unknown mode: {mode}. Use 'test' or 'full'.")
        return

    for year in years:
        sets = get_sets(year)
            
        for s in sets:
            set_name = s if s else 'AIME'
            print(f"Scraping {year} {set_name}")
            
            for i in problem_range:
                if s:
                    title = f"{year}_AIME_{s}_Problems/Problem_{i}"
                else:
                    title = f"{year}_AIME_Problems/Problem_{i}"
                    
                url = f"https://artofproblemsolving.com/wiki/index.php?title={title}"
                print(f"  Fetching {title}...")
                
                parsed_dict = scrape_problem_page(url)
                if parsed_dict:
                    data = {
                        'year': year,
                        'set': set_name,
                        'problem_number': i,
                        'url': url
                    }
                    # Merge structured data into the parent doc
                    data.update(parsed_dict)
                    dataset.append(data)
                time.sleep(1)  # Be nice to the server

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Extraction complete! Saved {len(dataset)} items to {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()