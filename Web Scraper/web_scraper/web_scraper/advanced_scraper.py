"""
Advanced Web Scraping Examples
Demonstrates pagination, form handling, and more complex scraping scenarios
"""

import requests
from bs4 import BeautifulSoup
from scraper import WebScraper
import time
from typing import List, Dict


class AdvancedScraper(WebScraper):
    """
    Extended scraper with advanced features
    """
    
    def scrape_with_pagination(self, start_url: str, config: Dict, 
                               next_selector: str = 'a.next', 
                               max_pages: int = 5) -> List[Dict]:
        """
        Scrape multiple pages following pagination links
        
        Args:
            start_url: Initial URL to start scraping
            config: Scraping configuration
            next_selector: CSS selector for the "next page" link
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of all scraped data
        """
        all_results = []
        current_url = start_url
        page_count = 0
        
        while current_url and page_count < max_pages:
            print(f"\nScraping page {page_count + 1}...")
            soup = self.fetch_page(current_url)
            
            if not soup:
                break
            
            # Extract data from current page
            result = {'page': page_count + 1, 'url': current_url}
            for key, selector in config.items():
                result[key] = self.extract_text(soup, selector)
            
            all_results.append(result)
            
            # Find next page link
            next_link = soup.select_one(next_selector)
            if next_link and next_link.get('href'):
                current_url = requests.compat.urljoin(current_url, next_link.get('href'))
                page_count += 1
                time.sleep(1)  # Be polite
            else:
                break
        
        return all_results
    
    def scrape_list_detail_pattern(self, list_url: str, 
                                   item_selector: str,
                                   link_selector: str,
                                   detail_config: Dict,
                                   max_items: int = 10) -> List[Dict]:
        """
        Scrape a list page and then detail pages for each item
        Common pattern: product listings, article listings, etc.
        
        Args:
            list_url: URL of the list page
            item_selector: CSS selector for list items
            link_selector: CSS selector for detail page link (relative to item)
            detail_config: Configuration for scraping detail pages
            max_items: Maximum number of items to scrape
            
        Returns:
            List of scraped detail data
        """
        soup = self.fetch_page(list_url)
        if not soup:
            return []
        
        # Extract links to detail pages
        items = soup.select(item_selector)[:max_items]
        detail_urls = []
        
        for item in items:
            link = item.select_one(link_selector)
            if link and link.get('href'):
                detail_urls.append(requests.compat.urljoin(list_url, link.get('href')))
        
        print(f"Found {len(detail_urls)} items to scrape")
        
        # Scrape each detail page
        return self.scrape_multiple_pages(detail_urls, detail_config, delay=1.0)
    
    def extract_structured_data(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract JSON-LD structured data from page
        Many modern websites include structured data in JSON-LD format
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of structured data objects
        """
        structured_data = []
        
        # Find all JSON-LD script tags
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                import json
                data = json.loads(script.string)
                structured_data.append(data)
            except:
                continue
        
        return structured_data
    
    def extract_by_xpath_like_pattern(self, soup: BeautifulSoup, 
                                      tag: str, 
                                      attrs: Dict = None) -> List:
        """
        Find elements by tag and attributes (XPath-like pattern)
        
        Args:
            soup: BeautifulSoup object
            tag: HTML tag name
            attrs: Dictionary of attributes to match
            
        Returns:
            List of matching elements
        """
        return soup.find_all(tag, attrs=attrs or {})
    
    def extract_nested_data(self, soup: BeautifulSoup, 
                           parent_selector: str,
                           child_configs: Dict[str, str]) -> List[Dict]:
        """
        Extract nested data structures
        Useful for cards, product listings, etc.
        
        Args:
            soup: BeautifulSoup object
            parent_selector: CSS selector for parent containers
            child_configs: Dictionary mapping keys to child selectors
            
        Returns:
            List of dictionaries with nested data
        """
        results = []
        parents = soup.select(parent_selector)
        
        for parent in parents:
            item = {}
            for key, selector in child_configs.items():
                elements = parent.select(selector)
                if elements:
                    if len(elements) == 1:
                        item[key] = elements[0].get_text(strip=True)
                    else:
                        item[key] = [elem.get_text(strip=True) for elem in elements]
            if item:
                results.append(item)
        
        return results


class NewsArticleScraper:
    """
    Specialized scraper for news articles
    """
    
    def __init__(self):
        self.scraper = AdvancedScraper("https://example.com")
    
    def scrape_article(self, url: str) -> Dict:
        """
        Scrape a news article with common patterns
        
        Args:
            url: Article URL
            
        Returns:
            Dictionary with article data
        """
        soup = self.scraper.fetch_page(url)
        if not soup:
            return {}
        
        article = {
            'url': url,
            'title': '',
            'author': '',
            'date': '',
            'content': [],
            'images': []
        }
        
        # Try common title selectors
        title_selectors = ['h1', 'article h1', '.article-title', 'h1.title']
        for selector in title_selectors:
            title = soup.select_one(selector)
            if title:
                article['title'] = title.get_text(strip=True)
                break
        
        # Try common author selectors
        author_selectors = ['.author', '.byline', '[rel="author"]', '.article-author']
        for selector in author_selectors:
            author = soup.select_one(selector)
            if author:
                article['author'] = author.get_text(strip=True)
                break
        
        # Try common date selectors
        date_selectors = ['time', '.date', '.publish-date', '[datetime]']
        for selector in date_selectors:
            date = soup.select_one(selector)
            if date:
                article['date'] = date.get('datetime') or date.get_text(strip=True)
                break
        
        # Extract article content
        content_selectors = ['article p', '.article-body p', '.content p', 'main p']
        for selector in content_selectors:
            paragraphs = soup.select(selector)
            if paragraphs:
                article['content'] = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                break
        
        # Extract images
        article['images'] = self.scraper.extract_images(soup)
        
        return article


def demo_advanced_scraping():
    """
    Demonstrate advanced scraping techniques
    """
    print("=" * 60)
    print("Advanced Web Scraping Demo")
    print("=" * 60)
    
    # Example 1: Scraping with pagination
    print("\nExample 1: Pagination scraping")
    print("-" * 60)
    
    scraper = AdvancedScraper("http://quotes.toscrape.com")
    
    config = {
        'quotes': '.quote .text',
        'authors': '.quote .author'
    }
    
    results = scraper.scrape_with_pagination(
        "http://quotes.toscrape.com/page/1/",
        config,
        next_selector='li.next a',
        max_pages=3
    )
    
    print(f"\nScraped {len(results)} pages")
    for i, page_data in enumerate(results, 1):
        print(f"Page {i}: Found {len(page_data.get('quotes', []))} quotes")
    
    # Example 2: Nested data extraction
    print("\n" + "=" * 60)
    print("Example 2: Extracting nested/structured data")
    print("-" * 60)
    
    soup = scraper.fetch_page("http://quotes.toscrape.com")
    if soup:
        nested_config = {
            'quote_text': '.text',
            'author': '.author',
            'tags': '.tag'
        }
        
        nested_data = scraper.extract_nested_data(soup, '.quote', nested_config)
        print(f"\nExtracted {len(nested_data)} structured quote objects")
        if nested_data:
            print(f"\nFirst quote object:")
            for key, value in nested_data[0].items():
                print(f"  {key}: {value}")
    
    # Example 3: Extract all links by type
    print("\n" + "=" * 60)
    print("Example 3: Categorizing links")
    print("-" * 60)
    
    if soup:
        all_links = scraper.extract_links(soup)
        
        # Categorize links
        internal_links = [link for link in all_links if 'quotes.toscrape.com' in link['url']]
        tag_links = [link for link in all_links if '/tag/' in link['url']]
        author_links = [link for link in all_links if '/author/' in link['url']]
        
        print(f"\nLink categories:")
        print(f"  Total links: {len(all_links)}")
        print(f"  Internal links: {len(internal_links)}")
        print(f"  Tag links: {len(tag_links)}")
        print(f"  Author links: {len(author_links)}")
    
    print("\n" + "=" * 60)
    print("Advanced scraping demo complete!")


if __name__ == "__main__":
    demo_advanced_scraping()
