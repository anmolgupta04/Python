# Web Scraper Project

A comprehensive Python web scraping toolkit using BeautifulSoup, requests, and other libraries. This project demonstrates various web scraping techniques and best practices for extracting data from websites.

## Features

- **Basic Web Scraping**: Extract text, links, images, and metadata
- **Advanced Scraping**: Pagination handling, nested data extraction, structured data
- **Specialized Scrapers**: Product pages, blog posts, news articles
- **Utilities**: Rate limiting, retry logic, caching, URL validation
- **Data Export**: JSON and CSV export functionality
- **Respectful Scraping**: Rate limiting, robots.txt support, proper headers

## Project Structure

```
web_scraper/
├── scraper.py              # Main scraper class with core functionality
├── advanced_scraper.py     # Advanced scraping techniques
├── practical_examples.py   # Real-world scraping examples
├── utils.py               # Utility functions and helpers
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Installation

1. Install required packages:

```bash
pip install beautifulsoup4 requests lxml --break-system-packages
```

2. All modules are ready to use!

## Quick Start

### Basic Usage

```python
from scraper import WebScraper

# Initialize scraper
scraper = WebScraper("https://example.com")

# Fetch a page
soup = scraper.fetch_page("https://example.com/page")

# Extract text from specific elements
titles = scraper.extract_text(soup, "h1")
paragraphs = scraper.extract_text(soup, "p")

# Extract links
links = scraper.extract_links(soup, "a")

# Extract images
images = scraper.extract_images(soup)
```

### Advanced Scraping

```python
from advanced_scraper import AdvancedScraper

scraper = AdvancedScraper("https://example.com")

# Scrape with pagination
config = {
    'title': 'h1',
    'content': 'p'
}

results = scraper.scrape_with_pagination(
    start_url="https://example.com/page/1",
    config=config,
    next_selector='a.next',
    max_pages=5
)

# Extract nested data
nested_data = scraper.extract_nested_data(
    soup,
    parent_selector='.card',
    child_configs={
        'title': '.card-title',
        'description': '.card-text',
        'price': '.price'
    }
)
```

### Practical Examples

```python
from practical_examples import ProductScraper, BlogScraper

# Scrape product information
product_scraper = ProductScraper("https://example-shop.com")
product = product_scraper.scrape_product("https://example-shop.com/product/123")

print(f"Name: {product['name']}")
print(f"Price: ${product['price']}")
print(f"Description: {product['description']}")

# Scrape blog posts
blog_scraper = BlogScraper()
post = blog_scraper.scrape_blog_post("https://example-blog.com/post/123")

print(f"Title: {post['title']}")
print(f"Author: {post['author']}")
print(f"Date: {post['date']}")
```

## Running Examples

Each module contains a demo function that can be run directly:

```bash
# Basic scraper demo
python scraper.py

# Advanced techniques demo
python advanced_scraper.py

# Practical examples demo
python practical_examples.py

# Utilities demo
python utils.py
```

## Key Features Explained

### 1. Rate Limiting

Automatically limit request frequency to be respectful to servers:

```python
from utils import rate_limiter

@rate_limiter(calls_per_second=2.0)
def scrape_page(url):
    # Your scraping code
    pass
```

### 2. Retry Logic

Automatically retry failed requests with exponential backoff:

```python
from utils import retry_on_failure

@retry_on_failure(max_attempts=3, delay=1.0, backoff=2.0)
def fetch_data(url):
    # Your fetching code
    pass
```

### 3. Data Caching

Cache scraped data to avoid redundant requests:

```python
from utils import DataCache

cache = DataCache()

# Check if data is cached
if cache.is_cached(url):
    data = cache.get(url)
else:
    data = scrape_data(url)
    cache.set(url, data)
```

### 4. Text Cleaning

Clean and process scraped text:

```python
from utils import TextCleaner

# Remove extra whitespace
clean_text = TextCleaner.clean_whitespace(dirty_text)

# Extract emails
emails = TextCleaner.extract_emails(text)

# Extract phone numbers
phones = TextCleaner.extract_phone_numbers(text)
```

### 5. URL Validation

Validate and normalize URLs:

```python
from utils import URLValidator

# Check if URL is valid
if URLValidator.is_valid_url(url):
    # Normalize URL
    clean_url = URLValidator.normalize_url(url, base_url)
    
    # Get domain
    domain = URLValidator.get_domain(url)
```

## Data Export

### Export to JSON

```python
scraper = WebScraper("https://example.com")

# Scrape data
data = scraper.scrape_multiple_pages(urls, config)

# Save to JSON
scraper.save_to_json(data, "output.json")
```

### Export to CSV

```python
# Save to CSV
scraper.save_to_csv(data, "output.csv")
```

## Best Practices

1. **Respect robots.txt**: Always check the site's robots.txt file
2. **Use rate limiting**: Don't overwhelm servers with requests
3. **Add delays**: Wait between requests (1-2 seconds is typical)
4. **Use proper headers**: Include a User-Agent header
5. **Handle errors gracefully**: Implement try-catch blocks
6. **Cache data**: Avoid redundant requests
7. **Check terms of service**: Ensure scraping is allowed
8. **Be ethical**: Don't scrape personal data or bypass authentication

## Common Patterns

### Pattern 1: List-Detail Scraping

Scrape a list page, then scrape detail pages for each item:

```python
scraper = AdvancedScraper("https://example.com")

results = scraper.scrape_list_detail_pattern(
    list_url="https://example.com/products",
    item_selector=".product-card",
    link_selector="a.product-link",
    detail_config={
        'name': 'h1',
        'price': '.price',
        'description': '.description'
    },
    max_items=10
)
```

### Pattern 2: Pagination

Automatically follow pagination links:

```python
results = scraper.scrape_with_pagination(
    start_url="https://example.com/page/1",
    config={'items': '.item'},
    next_selector='a.next-page',
    max_pages=10
)
```

### Pattern 3: Table Extraction

Extract data from HTML tables:

```python
table_data = scraper.extract_table(soup, 'table.data-table')

# Returns list of dictionaries with column headers as keys
for row in table_data:
    print(row)
```

## Troubleshooting

### Issue: Request timeout

```python
# Increase timeout
soup = scraper.fetch_page(url, timeout=30)
```

### Issue: Anti-scraping measures

```python
# Use custom headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/'
}

scraper = WebScraper(base_url, headers=headers)
```

### Issue: Dynamic content (JavaScript)

For JavaScript-rendered content, consider using Selenium or Playwright instead of requests/BeautifulSoup.

## Legal and Ethical Considerations

- Always check the website's Terms of Service
- Respect robots.txt directives
- Don't scrape copyrighted content without permission
- Avoid scraping personal or sensitive data
- Use rate limiting to avoid overloading servers
- Consider using official APIs when available

## Advanced Topics

### Custom Parsers

You can extend the base scraper for specific use cases:

```python
class MyCustomScraper(AdvancedScraper):
    def scrape_custom_content(self, url):
        soup = self.fetch_page(url)
        # Custom extraction logic
        return extracted_data
```

### Session Management

The scraper uses a session object for efficient connection pooling:

```python
scraper = WebScraper(base_url)
# Session is maintained across multiple requests
data1 = scraper.fetch_page(url1)
data2 = scraper.fetch_page(url2)  # Reuses connection
```

### Error Handling

Implement robust error handling:

```python
try:
    soup = scraper.fetch_page(url)
    if soup:
        data = scraper.extract_text(soup, selector)
    else:
        print(f"Failed to fetch {url}")
except Exception as e:
    print(f"Error: {e}")
```

## Contributing

Feel free to extend this project with additional features:
- Support for authentication
- Proxy rotation
- More specialized scrapers
- Additional export formats
- Database integration

## Resources

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://docs.python-requests.org/)
- [Web Scraping Best Practices](https://www.scrapinghub.com/blog/web-scraping-best-practices/)
- [CSS Selectors Reference](https://www.w3schools.com/cssref/css_selectors.asp)

## License

This project is for educational purposes. Always ensure you have permission to scrape websites and comply with their terms of service.
