from playwright.async_api import async_playwright
import os
import json
from utils import save_to_json
from categories import extract_categories
from professions import scrape_professions
from offers import scrape_offers
from jobs import scrape_job_details
import asyncio

async def handle_cookies(page):
    """
    Handle cookies popup if present and ensure it's fully dismissed.
    """
    try:
        cookies_button = page.locator("#pecookies-accept-all")
        if await cookies_button.is_visible():
            await cookies_button.click()
            print("Cookies accepted!")
        await page.wait_for_selector("#pecookies-accept-all", state="detached", timeout=5000)
    except Exception as e:
        print(f"No cookies modal found or already dismissed: {e}")

async def scrape_jobs_for_offers(page, offers, profession_name, category_name):
    """
    Scrape job details for a list of offers concurrently, adding profession and category metadata.
    """
    async def scrape_job(offer):
        job_url = offer["link"]
        try:
            print(f"Scraping job details for URL: {job_url}")
            job_details = await scrape_job_details(page, job_url)
            job_details["profession"] = profession_name
            job_details["category"] = category_name
            return job_details
        except Exception as e:
            print(f"Error scraping job at {job_url}: {e}")
            return None

    tasks = []
    for offer in offers:
        tasks.append(scrape_job(offer))     
        await asyncio.sleep(1)  


    job_details = await asyncio.gather(*tasks, return_exceptions=True)
    return [job for job in job_details if job is not None]

async def scrape_all():
    """
    Main function to scrape categories, professions, offers, and job details.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        page.set_default_timeout(60000)

        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        categories_path = "data/categories.json"
        if not os.path.exists(categories_path):
            print("Extracting categories...")
            await page.goto("https://candidat.francetravail.fr/offres/emploi")
            await handle_cookies(page)
            categories = await extract_categories(page)
            save_to_json(categories, categories_path)
        else:
            with open(categories_path, "r") as f:
                categories = json.load(f)

        for category in categories:
            category_name = category["name"]
            category_link = category["link"]
            professions_path = f"data/professions/{category_name.replace(' ', '_').lower()}_professions.json"

            if not os.path.exists(professions_path):
                professions = await scrape_professions(page, category_name, category_link)
                save_to_json(professions, professions_path)
            else:
                with open(professions_path, "r") as f:
                    professions = json.load(f)

            for profession in professions:
                profession_name = profession["name"]
                profession_link = profession["link"]

                print(f"Scraping offers for profession: {profession_name}")
                offers = await scrape_offers(page, profession_name, profession_link, max_offers=7, category_name=category_name)

                print(f"Scraping jobs for offers in profession: {profession_name}")
                jobs = await scrape_jobs_for_offers(page, offers, profession_name, category_name)

                job_path = f"data/jobs/{profession_name.replace(' ', '_').lower()}_jobs.json"
                save_to_json(jobs, job_path)
                print(f"Saved {len(jobs)} jobs for profession '{profession_name}'")

        await browser.close()

        


if __name__ == "__main__":
    asyncio.run(scrape_all())