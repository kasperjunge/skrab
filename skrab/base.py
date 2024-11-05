from abc import ABC, abstractmethod
import pandas as pd
from pathlib import Path

class BaseScraper(ABC):
    @abstractmethod
    def scrape_data(self) -> pd.DataFrame:
        """
        Abstract method to scrape data.

        Returns:
            pd.DataFrame: The scraped data as a pandas DataFrame.
        """
        pass

    def scrape_to_csv(self, output_file: Path) -> bool:
        """
        Scrape data and save to a CSV file.

        Args:
            output_file (Path): Path to save the CSV file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = self.scrape_data()
            output_file.parent.mkdir(parents=True, exist_ok=True)
            data.to_csv(output_file, index=False)
            return True
        except Exception as e:
            print(f"Error saving data to CSV: {e}")
            return False
