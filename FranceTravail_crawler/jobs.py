from playwright.async_api import Page

import asyncio


async def safe_get_text(page, selector, attribute=None):
    """
    Safely retrieves text or attribute value of a given selector.
    Returns None if the selector is not found or any exception occurs.
    """
    try:
        if attribute:
            return await page.locator(selector).get_attribute(attribute)
        return await page.locator(selector).inner_text()
    except Exception:
        return None

async def scrape_job_details(page: Page, job_url: str, retries=7):
    """
    Scrapes detailed job information from the given job URL.
    """
    for attempt in range(retries):
        try:
            await page.goto(job_url, wait_until="load")
            print(f"Opened job URL: {job_url}")

            job = {
                "reference": None,
                "name": None,
                "location": None,
                "date_posted": None,
                "description": None,
                "sections": [],
                "tags": [],
                "company": {},
                "additional_information": {}
            }

            # Extract basic fields
            job["reference"] = await safe_get_text(page, '[itemtype="http://schema.org/PropertyValue"] [itemprop="value"]')
            job["name"] = await safe_get_text(page, '[itemprop="title"]')
            job["location"] = await safe_get_text(page, '[itemtype="http://schema.org/PostalAddress"] [itemprop="name"]')
            job["date_posted"] = await safe_get_text(page, '[itemprop="datePosted"]', attribute="content")
            job["description"] = await safe_get_text(page, '[itemprop="description"]')

            # Extract profile background
            profile_title = await safe_get_text(page, 'h2.subtitle:has-text("Profil souhaité")')
            profile_description = await safe_get_text(page, '[itemprop="qualifications"]')
            experience = await safe_get_text(page, '[itemprop="experienceRequirements"]')
            if profile_title or profile_description:
                job["sections"].append({
                    "name": "profile_background",
                    "title": profile_title or "Profile Details",
                    "description": profile_description or "Not Provided",
                    "experience": experience or "Not Provided"
                })

            # Extract skills
            skills = []
            skill_elements = page.locator('[itemprop="skills"]')
            for i in range(await skill_elements.count()):
                skill_name = await skill_elements.nth(i).inner_text()
                if skill_name:
                    skills.append({"name": skill_name, "type": "soft"})
            if skills:
                job["sections"].append({"name": "skills", "skills": skills})

            # Extract tags (e.g., salary, contract type)
            salary = await safe_get_text(page, 'ul[style*="list-style-type: none"] > li:nth-child(1)')
            contract_type = await safe_get_text(page, '[itemprop="employmentType"]', attribute="content")
            if salary:
                job["tags"].append({"name": "salary", "value": salary})
            if contract_type:
                job["tags"].append({"name": "contract_type", "value": contract_type})

            # Extract company details
            company_name = await safe_get_text(page, '.media-body h3.title')
            company_size = await safe_get_text(page, '.media-body > p:first-child')
            contact_person = await safe_get_text(page, '.media-body .italic')
            job["company"] = {
                "name": company_name or "Unknown",
                "size": company_size or "Unknown",
                "contact_person": contact_person or "Unknown"
            }

            # Extract additional information
            qualification = await safe_get_text(page, '[itemprop="qualifications"]')
            industry = await safe_get_text(page, '[itemprop="industry"]')
            if qualification:
                job["additional_information"]["qualification"] = qualification
            if industry:
                job["additional_information"]["industry"] = industry

            return job

        except Exception as e:
            print(f"Error scraping job details at {job_url} on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(2)  # Retry after delay
            else:
                print(f"Failed to scrape job after {retries} attempts: {job_url}")
                return None
