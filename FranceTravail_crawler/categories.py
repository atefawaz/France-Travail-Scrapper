from playwright.async_api import async_playwright

async def extract_categories(page):
    """
    Extract job categories from the page.
    Exclude cities, regions, and job-specific links like `/s<number>m<number>`.
    """
    category_links = page.locator("a.media")
    category_data = []

    for i in range(await category_links.count()):
        category = category_links.nth(i)
        # Extract the category name and link
        name = await category.locator("span.media-body").inner_text()
        link = await category.get_attribute("href")

        # Filter logic:
        # 1. Include links that start with `/offres/emploi/`.
        # 2. Exclude links containing `/r` (regions) or `/v` (cities).
        # 3. Exclude links with `/s<number>m<number>`.
        if (
            link
            and link.startswith("/offres/emploi/")
            and "/r" not in link
            and "/v" not in link
            and "/s" in link
            and "m" not in link.split("/s")[-1]
        ):
            category_data.append({"name": name.strip(), "link": link})
            print(f"Extracted category: {name.strip()}, Link: {link}")  # Debugging log

    return category_data