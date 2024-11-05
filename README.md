# Skrab 🪒
## Overview
Skrab is a simple CLI and Python package for scraping various types of Danish data mainly for hobbyist use. The package is designed for flexibility, enabling you to contribute new scrapers and data sources as needed. With Skrab, you can build customized scrapers to collect data from public and private Danish resources and save it for analysis.

## Installation
Skrab is available on PyPI and can be installed via pip:

````bash
pip install skrab
````
## Usage
Running the Scraper
The skrab command-line interface (CLI) provides an easy way to run different scrapers. For example, to scrape real estate listings from Boliga and save them as a CSV file:

````bash
skrab boliga <output_file>.csv
````

Example:

````bash
skrab boliga data/boliga_listings.csv
````

This command will save Boliga listings to data/boliga_listings.csv.

## Extending Skrab
Coming soon..

