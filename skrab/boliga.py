import requests
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, List
from tqdm import tqdm

PAGE_SIZE = 500

class BoligaScraper:
    def __init__(self):
        self.base_url = "https://api.boliga.dk/api/v2/search/results"
        self.session = requests.Session()
        
    def fetch_listings(
        self,
        page: int = 1,
        page_size: int = PAGE_SIZE,
        searchGuid: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Fetch property listings from Boliga API synchronously.
        
        Args:
            page (int): Page number for pagination (default: 1)
            page_size (int): Number of results per page (default: 50)
        
        Returns:
            Optional[Dict]: JSON response from the API or None if request fails
        """
        sort = "daysForSale-a"  # Sorting parameter (default: "daysForSale-a")
        include_ds = True  # Include DS properties (default: True)
        include_otw = True  # Include OTW properties (default: True)

        params = {
            "pageSize": page_size,
            "sort": sort,
            "page": page,
            "includeds": int(include_ds),
            "includeotw": int(include_otw)
        }
        if searchGuid:
            params['searchGuid'] = searchGuid
        
        try:
            response = self.session.get(self.base_url, params=params)
            if response.status_code == 200:
                return response.json()
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching data from Boliga API: {e}")
            return None

    def scrape_to_csv(self, output_file: Path) -> bool:
        try:
            # Fetch the first page to get total_pages and searchGuid
            first_page = self.fetch_listings(page=1, page_size=PAGE_SIZE)
            if not first_page:
                return False
            
            total_pages = first_page['meta']['totalPages']
            searchGuid = first_page['meta']['searchGuid']
            
            # Ensure the output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert first page to DataFrame and write to CSV
            df = pd.DataFrame(first_page['results'])
            df.to_csv(output_file, index=False)
            total_listings = len(df)
            
            # Process remaining pages with tqdm progress bar
            pages = list(range(2, total_pages + 1))
            for page_num in tqdm(pages, desc="Fetching pages"):
                response = self.fetch_listings(page=page_num, page_size=PAGE_SIZE, searchGuid=searchGuid)
                if response and 'results' in response:
                    df = pd.DataFrame(response['results'])
                    df.to_csv(output_file, mode='a', header=False, index=False)
                    total_listings += len(df)
                else:
                    print(f"Failed to fetch page {page_num}")
            
            print(f"Successfully saved {total_listings} listings to {output_file}")
            return True
                
        except Exception as e:
            print(f"Error saving listings to CSV: {e}")
            return False
