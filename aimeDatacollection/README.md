# AIME Data Collection

This script automates the collection of AIME problems and solutions from the Art of Problem Solving wiki.

## Requirements

- Python 3.x
- requests
- beautifulsoup4

Install with: `pip install -r requirements.txt`

## Usage

Run the script: `python scrape_aime.py`

It will scrape all available AIME problems from 1983 to 2026 and save them to `aime_dataset.json`.

Each document in the JSON array has:
- year: The year of the AIME
- set: 'I', 'II', or 'AIME' for older years
- problem_number: 1-15
- problem_text: The problem statement
- solutions: List of solution texts
- notes: Any interesting notes
- video_links: List of video solution links

## Notes

- The script adds delays to be respectful to the server.
- Parsing is based on assumed HTML structure; may need adjustments if the wiki changes.
- For years without data, it will skip.