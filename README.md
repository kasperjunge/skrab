# Skrab
## Overview
Skrab is a Python package for scraping various types of Danish data, not limited to real estate. The package is designed for flexibility, enabling you to add new scrapers and data sources as needed. With Skrab, you can build customized scrapers to collect data from public and private Danish resources and save it for analysis.

Installation
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
### Adding New Scrapers
To add a new scraper for a different data source:

Create a New Scraper Module: In the skrab directory, create a new file, such as your_new_scraper.py, and define a class for handling data fetching and processing. Your scraper should include:

Fetch Method: To retrieve data from the source.
Output Method: To save the scraped data, usually in CSV format.
Update the CLI: Open cli.py and add a new command for the scraper:

Define a command function using @app.command().
Specify the necessary arguments and call your scraper class within this function.
Example:

````python
rom .your_new_scraper import YourNewScraper

@app.command()
def your_new_data(
    output_file: Annotated[Path, typer.Argument(help="Output CSV file path")]
):
    """Scrape your new data type and save to CSV."""
    scraper = YourNewScraper()
    success = scraper.scrape_to_csv(output_file)
    if success:
        typer.echo(f"Data saved to {output_file}")
    else:
        typer.echo("Failed to scrape data", err=True)
````

With this setup, users can run:

````bash
skrab your_new_data data/your_new_data.csv
````



