import typer
from pathlib import Path
from typing import Annotated
from .boliga import BoligaScraper

# Create app with no command as default
app = typer.Typer(no_args_is_help=True)

@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """
    Skrab - A tool for scraping Danish data.
    """
    if ctx.invoked_subcommand is None:
        typer.echo("Error: Please specify a command and path (e.g., 'skrab boliga output.csv')")
        raise typer.Exit(code=1)

@app.command()
def boliga(
    output_file: Annotated[
        Path, 
        typer.Argument(
            help="Path where to save the CSV file (must end in .csv)",
            exists=False,
            file_okay=True,
            dir_okay=False,
            writable=True,
            resolve_path=True,
        )
    ]
):
    """
    Scrape Boliga listings and save to CSV file.
    
    Args:
        output_file (Path): Path to save the CSV file
    """
    # Validate file extension
    if output_file.suffix.lower() != '.csv':
        typer.echo("Error: Output file must have .csv extension", err=True)
        raise typer.Exit(code=1)
        
    # Check if parent directory exists
    if not output_file.parent.exists():
        typer.echo(f"Error: Directory {output_file.parent} does not exist", err=True)
        raise typer.Exit(code=1)
    
    scraper = BoligaScraper()
    
    try:
        success = scraper.scrape_to_csv(output_file)
        if success:
            typer.echo(f"Successfully saved Boliga listings to {output_file}")
        else:
            typer.echo("Failed to scrape Boliga listings", err=True)
            raise typer.Exit(code=1)
    except KeyboardInterrupt:
        typer.echo("\nScraping cancelled by user", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error during scraping: {str(e)}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
