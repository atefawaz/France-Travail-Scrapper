# France Travail Scraper

A modular Python web scraper for extracting structured job-market data from France Travail using Playwright.

The project automates the collection of job categories, professions, job offers, and detailed job information through a multi-stage scraping pipeline, with support for concurrent processing and structured JSON output.

## Features

- **Category extraction** — Collects and filters job categories from France Travail.
- **Profession extraction** — Retrieves professions associated with each category.
- **Job offer scraping** — Collects available job offers for each profession.
- **Detailed job extraction** — Retrieves information including:
  - Job reference
  - Title and description
  - Location
  - Publication date
  - Candidate profile
  - Skills and tags
  - Company information
- **Concurrent scraping** — Processes multiple scraping tasks in parallel to improve execution time.
- **Structured data output** — Stores collected data as JSON for further processing or analysis.
- **Cookie handling** — Automatically manages cookie consent during browser sessions.

## How It Works

The scraper follows a multi-stage extraction process:

```text
France Travail
      │
      ▼
 Job Categories
      │
      ▼
  Professions
      │
      ▼
  Job Offers
      │
      ▼
 Job Details
      │
      ▼
Structured JSON
```

Each stage is handled by a dedicated module, keeping the scraping logic separated and reusable.

## Project Structure

```text
.
├── FranceTravail_scraper/
│   ├── __init__.py
│   ├── categories.py       # Category extraction
│   ├── professions.py      # Profession extraction
│   ├── offers.py           # Job offer extraction
│   ├── jobs.py             # Detailed job information
│   ├── scraper.py          # Scraping pipeline and orchestration
│   └── utils.py            # Shared utility functions
│
├── data/                   # Generated scraped data
└── README.md
```

## Technologies

- **Python**
- **Playwright**
- **Browser Automation**
- **Concurrent Processing**
- **JSON**

## Installation

### Prerequisites

- Python 3.8+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/atefawaz/France-Travail-Scrapper.git
cd France-Travail-Scrapper
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install Playwright

```bash
pip install playwright
playwright install
```

## Usage

Run the scraper to start the extraction pipeline:

```bash
python3 FranceTravail_scraper/scraper.py
```

The scraper processes the different stages sequentially, from job categories to detailed job information.

## Data Output

Collected data is stored in the `data/` directory.

```text
data/
├── categories.json
├── professions/
├── offers/
└── jobs/
```

The JSON output can be reused for further processing, analysis, or other applications.

## Configuration

The scraper can be configured directly from `scraper.py`.

### Maximum Offers

Modify the `max_offers` parameter to control the number of job offers processed.

### Browser Mode

Playwright can run with or without a visible browser window by changing the `headless` configuration.

```python
headless=True
```

### Timeouts

Playwright timeout values can be adjusted in `scraper.py` depending on network conditions and page-loading times.

## Technical Challenges

This project involved working with dynamically rendered web pages rather than relying only on static HTML requests.

Some of the main challenges addressed include:

- Navigating multiple levels of related job-market data.
- Automating interactions with dynamically loaded pages.
- Managing browser sessions and cookie consent.
- Extracting and organizing information from different page structures.
- Processing multiple scraping operations concurrently.
- Persisting collected information in a reusable structured format.

The scraper was organized into separate modules for each stage of the extraction process to keep the code easier to maintain and extend.

## Disclaimer

This project was developed for educational and technical experimentation purposes.

Websites may change their structure over time, which can affect scraper functionality. Users are responsible for ensuring that their use of the scraper complies with applicable terms of service, robots policies, rate limits, and regulations.

## Author

**Atef Fawaz**

GitHub: [@atefawaz](https://github.com/atefawaz)
