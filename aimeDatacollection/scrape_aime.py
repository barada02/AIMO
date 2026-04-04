import requests
from bs4 import BeautifulSoup
import json
import time
import os

BASE_URL = "https://artofproblemsolving.com/wiki/index.php?title=AIME_Problems_and_Solutions"
OUTPUT_FILE = "aime_dataset.json"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def scrape_main_page():
    soup = get_soup(BASE_URL)
    table = soup.find('table')  # Assuming the table is the first one
    rows = table.find_all('tr')[1:]  # Skip header

    years_data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 3:  # Year, Test I, Test II
            year = cells[0].text.strip()
            test_i_link = cells[1].find('a')['href'] if cells[1].find('a') else None
            test_ii_link = cells[2].find('a')['href'] if cells[2].find('a') else None
            years_data.append({
                'year': year,
                'sets': [
                    {'name': 'I', 'link': test_i_link},
                    {'name': 'II', 'link': test_ii_link}
                ]
            })
        elif len(cells) == 2:  # Year, AIME
            year = cells[0].text.strip()
            aime_link = cells[1].find('a')['href'] if cells[1].find('a') else None
            years_data.append({
                'year': year,
                'sets': [
                    {'name': 'AIME', 'link': aime_link}
                ]
            })
    return years_data

def scrape_set_page(set_url):
    soup = get_soup(set_url)
    content = soup.find('div', {'id': 'mw-content-text'})
    if not content:
        print("No content div found")
        return []

    print(f"Found content div, length: {len(content.text)}")

    # Find all headlines
    headlines = []
    for h in content.find_all(['h2', 'h3']):
        span = h.find('span', class_='mw-headline')
        if span:
            headlines.append(span.text)
    print(f"Headlines found: {headlines}")

    problems = []
    current_problem = None
    current_content = []

    for element in content.find_all(['h2', 'h3', 'p', 'ol', 'ul', 'div']):
        if element.name in ['h2', 'h3']:
            headline = element.find('span', class_='mw-headline')
            if headline and 'Problem' in headline.text:
                if current_problem:
                    problems.append((current_problem, current_content))
                current_problem = headline.text
                current_content = []
                print(f"Found problem: {current_problem}")
            elif current_problem:
                current_content.append(element)
        elif current_problem:
            current_content.append(element)

    if current_problem:
        problems.append((current_problem, current_content))

    print(f"Total problems found: {len(problems)}")
    return problems[:15]  # Take first 15

def parse_problem_content(content_elements):
    problem_text = ""
    solutions = []
    notes = ""
    video_links = []

    text = '\n'.join([elem.text for elem in content_elements])

    # Simple parsing
    lines = text.split('\n')
    in_solution = False
    current_solution = ""
    for line in lines:
        if 'Solution' in line and any(char.isdigit() for char in line):
            if current_solution:
                solutions.append(current_solution.strip())
            current_solution = line + '\n'
            in_solution = True
        elif in_solution:
            current_solution += line + '\n'
        elif not problem_text and line.strip():
            problem_text = line.strip()
        elif 'Note' in line.lower():
            notes = line
        elif 'video' in line.lower() or 'youtube' in line.lower():
            # Find links
            pass

    if current_solution:
        solutions.append(current_solution.strip())

    # Find video links from elements
    for elem in content_elements:
        for a in elem.find_all('a', href=True):
            if 'youtube' in a['href'] or 'video' in a['href']:
                video_links.append(a['href'])

    return {
        'problem_text': problem_text,
        'solutions': solutions,
        'notes': notes,
        'video_links': video_links
    }

def main():
    years_data = scrape_main_page()
    dataset = []

    for year_info in years_data:
        year = year_info['year']
        for set_info in year_info['sets']:
            if not set_info['link']:
                continue
            set_url = "https://artofproblemsolving.com" + set_info['link']
            print(f"Scraping {year} {set_info['name']}")
            problems = scrape_set_page(set_url)
            for prob_title, content in problems:
                prob_num = int(prob_title.split()[-1])
                data = parse_problem_content(content)
                doc = {
                    'year': year,
                    'set': set_info['name'],
                    'problem_number': prob_num,
                    **data
                }
                dataset.append(doc)
                time.sleep(1)  # Be nice to the server

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(dataset, f, indent=2)

if __name__ == "__main__":
    main()