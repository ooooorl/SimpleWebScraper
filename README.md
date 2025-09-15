# **Project: Job Scraper**

This project is a simple web scraper designed to extract job information and save it to a CSV file.

## 📂 File Structure

- **scraper.py**: The main Python script that contains the scraping logic. It fetches job data from a specified website.
- **comprehensive_jobs.csv**: The output file where the scraped job data is stored. Each row represents a job with relevant details.
- **requirements/base.txt**: A file listing all the necessary Python libraries to run the scraper.
- **README.md**: This document, providing an overview of the project and instructions for use.

## ⚙️ Requirements

- Python 3.x installed on your system.
- Project dependencies listed in `requirements/base.txt`.

Execute the following commands:

```bash
python3.13 -m virtualenv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements/base.txt
```

Run the Script
```bash
python scraper.py
```
