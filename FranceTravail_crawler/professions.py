from playwright.async_api import async_playwright
from utils import save_to_json

import os

async def scrape_professions(page, category_name, category_link):
    """
    Scrape professions for a given category.
    """
    await page.goto(f"https://candidat.francetravail.fr{category_link}")
    await page.wait_for_load_state("networkidle")

    # Locate professions
    profession_links = page.locator("a.media")  # Replace with the actual selector
    professions = []

    for i in range(await profession_links.count()):
        try:
            profession = profession_links.nth(i)
            # Check if the span exists
            if not await profession.locator("span.media-body").is_visible():
                continue
            
            # Extract profession name and link
            name = await profession.locator("span.media-body").inner_text(timeout=5000)
            link = await profession.get_attribute("href")

            # Filter: Ensure link matches the profession pattern
            if link and "/s" in link and "m" in link.split("/s")[-1]:
                professions.append({
                    "name": name.strip(),
                    "link": f"https://candidat.francetravail.fr{link}"
                })
                print(f"Extracted profession: {name.strip()}, Link: {link}")

        except Exception as e:
            print(f"Error extracting profession at index {i}: {e}")

    # Save professions to a file
    os.makedirs(f"data/professions", exist_ok=True)
    filepath = f"data/professions/{category_name.replace(' ', '_').lower()}_professions.json"
    save_to_json(professions, filepath)

    print(f"Professions for '{category_name}' saved to {filepath}")

    return professions