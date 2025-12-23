"""
Local Web Scraping Demo
Demonstrates scraping techniques using a local HTML file
"""

from bs4 import BeautifulSoup
from scraper import WebScraper
from advanced_scraper import AdvancedScraper
from utils import TextCleaner, URLValidator, DataCache
import json


def load_local_html(filepath: str) -> BeautifulSoup:
    """Load and parse local HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return BeautifulSoup(html_content, 'lxml')


def demo_basic_scraping():
    """Demonstrate basic scraping techniques"""
    print("=" * 70)
    print("BASIC WEB SCRAPING DEMO")
    print("=" * 70)
    
    # Load local HTML
    soup = load_local_html('sample_page.html')
    
    # Example 1: Extract all headings
    print("\n1. Extracting Headings:")
    print("-" * 70)
    headings = {}
    for i in range(1, 4):
        tags = soup.find_all(f'h{i}')
        headings[f'h{i}'] = [tag.get_text(strip=True) for tag in tags]
    
    for level, texts in headings.items():
        if texts:
            print(f"\n{level.upper()} tags ({len(texts)} found):")
            for text in texts:
                print(f"  - {text}")
    
    # Example 2: Extract product information
    print("\n\n2. Extracting Product Information:")
    print("-" * 70)
    
    products = soup.select('article.product_pod')
    print(f"\nFound {len(products)} products:\n")
    
    for i, product in enumerate(products, 1):
        title = product.select_one('h3 a')
        price = product.select_one('.price_color')
        availability = product.select_one('.availability')
        description = product.select_one('.description')
        tags = product.select('.tag')
        
        print(f"Product {i}:")
        print(f"  Title: {title.get('title') if title else 'N/A'}")
        print(f"  Price: {price.get_text(strip=True) if price else 'N/A'}")
        print(f"  Availability: {availability.get_text(strip=True) if availability else 'N/A'}")
        print(f"  Description: {description.get_text(strip=True) if description else 'N/A'}")
        print(f"  Tags: {[tag.get_text(strip=True) for tag in tags]}")
        print()
    
    # Example 3: Extract all links
    print("\n3. Extracting Links:")
    print("-" * 70)
    
    links = soup.find_all('a')
    print(f"\nFound {len(links)} links:\n")
    
    # Categorize links
    nav_links = [link for link in links if link.find_parent('nav')]
    product_links = [link for link in links if '/products/' in str(link.get('href', ''))]
    tag_links = [link for link in links if '/tag/' in str(link.get('href', ''))]
    
    print(f"Navigation links: {len(nav_links)}")
    for link in nav_links:
        print(f"  - {link.get_text(strip=True)}: {link.get('href')}")
    
    print(f"\nProduct links: {len(product_links)}")
    for link in product_links[:3]:
        print(f"  - {link.get('title', link.get_text(strip=True))}: {link.get('href')}")
    
    print(f"\nTag links: {len(tag_links)}")
    for link in tag_links:
        print(f"  - {link.get_text(strip=True)}: {link.get('href')}")
    
    # Example 4: Extract images
    print("\n\n4. Extracting Images:")
    print("-" * 70)
    
    images = soup.find_all('img')
    print(f"\nFound {len(images)} images:\n")
    
    for img in images:
        print(f"  Source: {img.get('src')}")
        print(f"  Alt text: {img.get('alt')}")
        print(f"  Title: {img.get('title', 'N/A')}")
        print()
    
    # Example 5: Extract table data
    print("\n5. Extracting Table Data:")
    print("-" * 70)
    
    table = soup.select_one('table.product-specs')
    if table:
        caption = table.find('caption')
        print(f"\nTable: {caption.get_text(strip=True) if caption else 'Unnamed'}\n")
        
        rows = table.select('tbody tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) == 2:
                print(f"  {cells[0].get_text(strip=True)}: {cells[1].get_text(strip=True)}")


def demo_advanced_scraping():
    """Demonstrate advanced scraping techniques"""
    print("\n\n" + "=" * 70)
    print("ADVANCED WEB SCRAPING DEMO")
    print("=" * 70)
    
    soup = load_local_html('sample_page.html')
    scraper = AdvancedScraper("file://")
    
    # Example 1: Extract nested/structured data
    print("\n1. Extracting Nested Product Data:")
    print("-" * 70)
    
    nested_config = {
        'title': 'h3 a',
        'price': '.price_color',
        'availability': '.availability',
        'description': '.description',
        'tags': '.tag'
    }
    
    products_data = scraper.extract_nested_data(soup, 'article.product_pod', nested_config)
    
    print(f"\nExtracted {len(products_data)} structured product objects:\n")
    for i, product in enumerate(products_data, 1):
        print(f"Product {i}:")
        print(json.dumps(product, indent=2))
        print()
    
    # Example 2: Extract blog posts
    print("\n2. Extracting Blog Post Data:")
    print("-" * 70)
    
    blog_config = {
        'title': 'h3 a',
        'author': '.author',
        'date': 'time',
        'excerpt': '.excerpt',
        'categories': '.categories a'
    }
    
    blog_posts = scraper.extract_nested_data(soup, 'article.post', blog_config)
    
    print(f"\nExtracted {len(blog_posts)} blog posts:\n")
    for i, post in enumerate(blog_posts, 1):
        print(f"Post {i}:")
        print(json.dumps(post, indent=2))
        print()
    
    # Example 3: Extract metadata
    print("\n3. Extracting Page Metadata:")
    print("-" * 70)
    
    metadata = scraper.extract_metadata(soup)
    print("\nPage metadata:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")


def demo_utilities():
    """Demonstrate utility functions"""
    print("\n\n" + "=" * 70)
    print("UTILITIES DEMO")
    print("=" * 70)
    
    soup = load_local_html('sample_page.html')
    
    # Example 1: Text cleaning
    print("\n1. Text Cleaning:")
    print("-" * 70)
    
    contact_section = soup.select_one('.contact-info')
    if contact_section:
        text = contact_section.get_text()
        
        # Extract emails
        emails = TextCleaner.extract_emails(text)
        print(f"\nEmails found: {emails}")
        
        # Extract phone numbers
        phones = TextCleaner.extract_phone_numbers(text)
        print(f"Phone numbers found: {phones}")
        
        # Clean whitespace
        paragraphs = contact_section.find_all('p')
        for p in paragraphs:
            original = p.get_text()
            cleaned = TextCleaner.clean_whitespace(original)
            if original != cleaned:
                print(f"\nOriginal: '{original}'")
                print(f"Cleaned: '{cleaned}'")
    
    # Example 2: URL validation
    print("\n\n2. URL Validation:")
    print("-" * 70)
    
    test_urls = [
        "https://example.com/products/laptop",
        "/products/mouse",
        "not-a-url",
        "ftp://files.example.com/data.txt"
    ]
    
    print("\nTesting URLs:")
    for url in test_urls:
        is_valid = URLValidator.is_valid_url(url)
        normalized = URLValidator.normalize_url(url, "https://example.com")
        print(f"  {url}")
        print(f"    Valid: {is_valid}")
        print(f"    Normalized: {normalized}")
    
    # Example 3: Caching demonstration
    print("\n\n3. Data Caching:")
    print("-" * 70)
    
    cache = DataCache()
    test_url = "https://example.com/product/123"
    test_data = {
        "name": "Sample Product",
        "price": 99.99,
        "in_stock": True
    }
    
    print(f"\nIs '{test_url}' cached? {cache.is_cached(test_url)}")
    
    cache.set(test_url, test_data)
    print(f"After caching: {cache.is_cached(test_url)}")
    
    retrieved = cache.get(test_url)
    print(f"\nRetrieved data:")
    print(json.dumps(retrieved['data'], indent=2))


def demo_data_export():
    """Demonstrate data export functionality"""
    print("\n\n" + "=" * 70)
    print("DATA EXPORT DEMO")
    print("=" * 70)
    
    soup = load_local_html('sample_page.html')
    scraper = AdvancedScraper("file://")
    
    # Extract product data
    nested_config = {
        'title': 'h3 a',
        'price': '.price_color',
        'availability': '.availability',
        'description': '.description'
    }
    
    products_data = scraper.extract_nested_data(soup, 'article.product_pod', nested_config)
    
    # Export to JSON
    print("\n1. Exporting to JSON:")
    print("-" * 70)
    scraper.save_to_json(products_data, 'products.json')
    
    # Export to CSV
    print("\n2. Exporting to CSV:")
    print("-" * 70)
    scraper.save_to_csv(products_data, 'products.csv')
    
    # Show file contents
    print("\n3. Generated Files:")
    print("-" * 70)
    
    print("\nJSON file content (first 500 chars):")
    with open('products.json', 'r') as f:
        content = f.read()
        print(content[:500] + "..." if len(content) > 500 else content)
    
    print("\n\nCSV file content:")
    with open('products.csv', 'r') as f:
        print(f.read())


def main():
    """Run all demos"""
    demo_basic_scraping()
    demo_advanced_scraping()
    demo_utilities()
    demo_data_export()
    
    print("\n\n" + "=" * 70)
    print("ALL DEMOS COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - products.json")
    print("  - products.csv")
    print("\nYou can now use these scraping techniques on real websites!")
    print("Remember to always respect robots.txt and terms of service.")


if __name__ == "__main__":
    main()
