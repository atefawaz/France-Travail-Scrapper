
# France Travail Scraper

## Overview

The **France Travail Scraper** is a robust web scraping framework designed to extract job-related data from the France Travail website. It utilizes Playwright for efficient, concurrent, and structured scraping of categories, professions, job offers, and detailed job information.

---

## Features

1. **Category Extraction**: Extracts and filters job categories from the website.
2. **Profession Scraping**: Retrieves professions for each category.
3. **Job Offers Scraping**: Scrapes job offers including title, company, location, and description.
4. **Job Details Extraction**: Gathers detailed job information such as:
   - Reference
   - Title and Description
   - Location
   - Date Posted
   - Profile Background
   - Skills and Tags
   - Company Information
5. **Concurrency**: Optimized for parallel scraping to save time.
6. **Data Persistence**: Saves data as JSON files for easy reuse.
7. **Cookie Management**: Automatically handles cookie consent popups.

---

## Directory Structure

```
.
├── FranceTravail_scraper
│   ├── __init__.py
│   ├── categories.py       # Handles category extraction
│   ├── jobs.py             # Scrapes detailed job information
│   ├── offers.py           # Extracts job offers for professions
│   ├── professions.py      # Retrieves professions for categories
│   ├── scraper.py          # Main orchestrator script
│   ├── utils.py            # Utility functions (e.g., save_to_json)
├── README.md               # Project documentation
└── data/                   # Directory for storing scraped data
```

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/atefawaz/France-Travail-Scrapper.git
   cd FranceTravail_crawler
   ```


2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install playwright
   playwright install
   ```


---

## Usage

### Running the Scraper

To scrape all categories, professions, offers, and job details:
```bash
python3 scraper.py
```

### Data Output

Scraped data will be saved in the `data/` directory:
- **Categories**: `data/categories.json`
- **Professions**: `data/professions/`
- **Offers**: `data/offers/`
- **Jobs**: `data/jobs/`

---

## Configuration

- **Max Offers**: Limit the number of job offers scraped by modifying the `max_offers` parameter in `scraper.py`.
- **Timeouts**: Adjust Playwright timeouts in the `scraper.py` file.
- **Headless Mode**: Enable or disable headless mode in the `scraper.py` file by changing `headless=False` to `headless=True`.

---

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- **Playwright**: For providing a reliable browser automation framework.
- **France Travail**: For the inspiration behind this project.
- Open-source contributors for their valuable libraries.

---

## Contact

For questions, issues, or feedback, please contact:

**Your Name**  
GitHub: [atefawaz](https://github.com/atefawaz)
