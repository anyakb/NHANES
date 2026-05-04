"""
NHANES Web Scraping Script
===========================
Scrapes WHO/Mental Health Foundation statistics on income and mental health
to contextualise NHANES findings in the blog.

Input:  Live web pages (Mental Health Foundation, WHO)
Output: outputs/tables/scraped_context.csv
        outputs/tables/scraped_context.txt (human-readable summary)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

os.makedirs('outputs/tables', exist_ok=True)


# Helper function to scrape a page

def scrape_page(url, source_name):
    """Scrape paragraph text from a given URL."""
    headers = {'User-Agent': 'Mozilla/5.0 (educational research project)'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all paragraph text
        paragraphs = soup.find_all('p')
        text_blocks = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            # Only keep meaningful sentences (not nav links etc.)
            if len(text) > 60:
                text_blocks.append({
                    'source': source_name,
                    'url': url,
                    'text': text
                })
        print(f"✓ Scraped {len(text_blocks)} passages from {source_name}")
        return text_blocks

    except Exception as e:
        print(f"✗ Failed to scrape {source_name}: {e}")
        return []


# Pages to scrape
sources = [
    {
        'url': 'https://www.mentalhealth.org.uk/explore-mental-health/statistics/social-determinants-statistics',
        'name': 'Mental Health Foundation — Social Determinants'
    },
    {
        'url': 'https://www.who.int/teams/social-determinants-of-health/equity-and-health/world-report-on-social-determinants-of-health-equity',
        'name': 'WHO — World Report on Social Determinants'
    },
    {
        'url': 'https://mhanational.org/resources/social-determinants-of-health/',
        'name': 'Mental Health America — Social Determinants'
    }
]


# Run scraper
all_results = []

for source in sources:
    results = scrape_page(source['url'], source['name'])
    all_results.extend(results)
    time.sleep(2)  # polite delay between requests


# Save results

if all_results:
    df = pd.DataFrame(all_results)
    df.to_csv('outputs/tables/scraped_context.csv', index=False)
    print(f"\nSaved {len(df)} passages to outputs/tables/scraped_context.csv")

    # Also save a clean readable text summary
    with open('outputs/tables/scraped_context.txt', 'w', encoding='utf-8') as f:
        f.write("SCRAPED CONTEXT: Income, Social Determinants & Mental Health\n")
        f.write("=" * 60 + "\n\n")
        for source_name in df['source'].unique():
            f.write(f"SOURCE: {source_name}\n")
            f.write("-" * 40 + "\n")
            source_rows = df[df['source'] == source_name]
            for _, row in source_rows.iterrows():
                f.write(f"{row['text']}\n\n")
            f.write("\n")

    print("Saved readable summary to outputs/tables/scraped_context.txt")

else:
    print("No results scraped. Check for errors in the scraping process.")