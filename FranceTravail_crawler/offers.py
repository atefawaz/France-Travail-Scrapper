import asyncio  # Add this line
from utils import save_to_json
import json
import os

async def scrape_offers(page, profession_name, profession_link, max_offers=None, category_name=None):
    """
    Scrape up to 'max_offers' offers for a given profession, or all if max_offers is None.
    """
    offers = []
    base_url = "https://candidat.francetravail.fr"
    full_url = profession_link if profession_link.startswith("http") else f"{base_url}{profession_link}"

    await page.goto(full_url)
    await page.wait_for_load_state("networkidle")

    # Create the offers folder if it doesn't exist
    offers_folder = "data/offers"
    os.makedirs(offers_folder, exist_ok=True)

    while max_offers is None or len(offers) < max_offers:
        offer_cards = page.locator("a.media.with-fav")
        for i in range(await offer_cards.count()):
            if max_offers and len(offers) >= max_offers:
                break
            try:
                offer = offer_cards.nth(i)
                title = await offer.locator(".media-heading-title").inner_text()
                company = await offer.locator(".subtext").inner_text()
                location = await offer.locator(".subtext > span").inner_text()
                link = await offer.get_attribute("href")
                description = await offer.locator(".description").inner_text()

                offers.append({
                    "title": title.strip(),
                    "company": company.strip(),
                    "location": location.strip(),
                    "description": description.strip(),
                    "link": f"{base_url}{link}",
                    "profession": profession_name,
                    "category": category_name
                })
            except Exception as e:
                print(f"Error extracting offer: {e}")

        next_button = page.locator("a.btn.btn-primary[href*='afficherplusderesultats']")
        if await next_button.is_visible():
            try:
                await next_button.click()
                await asyncio.sleep(1)  # Add a delay to prevent rate-limiting
                await page.wait_for_load_state("networkidle")
            except Exception as e:
                print(f"Error clicking pagination button: {e}")
                break
        else:
            break

    offers_file = f"{offers_folder}/{profession_name.replace(' ', '_').lower()}_offers.json"
    with open(offers_file, "w") as f:
        json.dump(offers, f, indent=4)

    print(f"Scraped {len(offers)} offers for profession '{profession_name}'")
    return offers
