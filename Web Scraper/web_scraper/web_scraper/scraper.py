"""
Web Scraper Module
A comprehensive web scraping tool using BeautifulSoup and requests
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse


class WebScraper:
    """
    A flexible web scraper class that can extract data from websites
    """
    
    def __init__(self, base_url: str, headers: Optional[Dict] = None):
        """
        Initialize the scraper with a base URL
        
        Args:
            base_url: The base URL to scrape
            headers: Optional custom headers for requests
        """
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch_page(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        """
        Fetch a web page and return BeautifulSoup object
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            BeautifulSoup object or None if request fails
        """
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_text(self, soup: BeautifulSoup, selector: str) -> List[str]:
        """
        Extract text from elements matching CSS selector
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector string
            
        Returns:
            List of text content
        """
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]
    
    def extract_links(self, soup: BeautifulSoup, selector: str = 'a') -> List[Dict[str, str]]:
        """
        Extract links from the page
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector for link elements
            
        Returns:
            List of dictionaries with 'text' and 'url' keys
        """
        links = []
        for link in soup.select(selector):
            href = link.get('href')
            if href:
                absolute_url = urljoin(self.base_url, href)
                links.append({
                    'text': link.get_text(strip=True),
                    'url': absolute_url
                })
        return links
    
    def extract_images(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """
        Extract image URLs and alt text
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of dictionaries with image data
        """
        images = []
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src:
                images.append({
                    'url': urljoin(self.base_url, src),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
        return images
    
    def extract_table(self, soup: BeautifulSoup, table_selector: str = 'table') -> List[Dict]:
        """
        Extract data from HTML tables
        
        Args:
            soup: BeautifulSoup object
            table_selector: CSS selector for the table
            
        Returns:
            List of dictionaries representing table rows
        """
        table = soup.select_one(table_selector)
        if not table:
            return []
        
        headers = []
        header_row = table.find('thead')
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
        else:
            # Try to get headers from first row
            first_row = table.find('tr')
            if first_row:
                headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])]
        
        rows = []
        tbody = table.find('tbody') or table
        for row in tbody.find_all('tr')[1 if not table.find('thead') else 0:]:
            cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
            if cells:
                if headers and len(headers) == len(cells):
                    rows.append(dict(zip(headers, cells)))
                else:
                    rows.append({'data': cells})
        
        return rows
    
    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract metadata from page (title, meta tags, etc.)
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Dictionary of metadata
        """
        metadata = {}
        
        # Title
        if soup.title:
            metadata['title'] = soup.title.get_text(strip=True)
        
        # Meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content
        
        return metadata
    
    def scrape_page(self, url: str, config: Dict) -> Dict:
        """
        Scrape a page based on configuration
        
        Args:
            url: URL to scrape
            config: Dictionary with selectors for different elements
                   Example: {
                       'title': 'h1',
                       'paragraphs': 'p',
                       'links': 'a.external-link'
                   }
        
        Returns:
            Dictionary with scraped data
        """
        soup = self.fetch_page(url)
        if not soup:
            return {}
        
        result = {'url': url}
        
        for key, selector in config.items():
            if key == 'links':
                result[key] = self.extract_links(soup, selector)
            elif key == 'images':
                result[key] = self.extract_images(soup)
            elif key == 'table':
                result[key] = self.extract_table(soup, selector)
            elif key == 'metadata':
                result[key] = self.extract_metadata(soup)
            else:
                result[key] = self.extract_text(soup, selector)
        
        return result
    
    def scrape_multiple_pages(self, urls: List[str], config: Dict, delay: float = 1.0) -> List[Dict]:
        """
        Scrape multiple pages with rate limiting
        
        Args:
            urls: List of URLs to scrape
            config: Scraping configuration
            delay: Delay between requests in seconds
            
        Returns:
            List of scraped data dictionaries
        """
        results = []
        for i, url in enumerate(urls):
            print(f"Scraping {i+1}/{len(urls)}: {url}")
            result = self.scrape_page(url, config)
            if result:
                results.append(result)
            
            # Be polite - add delay between requests
            if i < len(urls) - 1:
                time.sleep(delay)
        
        return results
    
    def save_to_json(self, data: List[Dict], filename: str):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")
    
    def save_to_csv(self, data: List[Dict], filename: str):
        """Save scraped data to CSV file"""
        if not data:
            print("No data to save")
            return
        
        # Flatten nested dictionaries for CSV
        flattened_data = []
        for item in data:
            flat_item = {}
            for key, value in item.items():
                if isinstance(value, (list, dict)):
                    flat_item[key] = json.dumps(value)
                else:
                    flat_item[key] = value
            flattened_data.append(flat_item)
        
        keys = flattened_data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(flattened_data)
        print(f"Data saved to {filename}")


def main():
    """
    Example usage of the WebScraper class
    """
    print("=" * 60)
    print("Web Scraper Demo")
    print("=" * 60)
    
    # Example 1: Scrape quotes from quotes.toscrape.com
    print("\nExample 1: Scraping quotes...")
    scraper = WebScraper("http://quotes.toscrape.com")
    
    config = {
        'quotes': '.quote .text',
        'authors': '.quote .author',
        'tags': '.quote .tags .tag'
    }
    
    result = scraper.scrape_page("http://quotes.toscrape.com", config)
    
    if result:
        print(f"\nFound {len(result.get('quotes', []))} quotes")
        if result.get('quotes'):
            print(f"\nFirst quote: {result['quotes'][0]}")
            print(f"First author: {result['authors'][0]}")
    
    # Example 2: Extract links from a page
    print("\n" + "=" * 60)
    print("Example 2: Extracting links...")
    
    soup = scraper.fetch_page("http://quotes.toscrape.com")
    if soup:
        links = scraper.extract_links(soup, 'a')
        print(f"\nFound {len(links)} links")
        if links:
            print(f"First 3 links:")
            for link in links[:3]:
                print(f"  - {link['text']}: {link['url']}")
    
    # Example 3: Extract metadata
    print("\n" + "=" * 60)
    print("Example 3: Extracting metadata...")
    
    if soup:
        metadata = scraper.extract_metadata(soup)
        print(f"\nPage metadata:")
        for key, value in metadata.items():
            print(f"  {key}: {value[:100]}..." if len(value) > 100 else f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("Scraping complete!")


if __name__ == "__main__":
    main()
