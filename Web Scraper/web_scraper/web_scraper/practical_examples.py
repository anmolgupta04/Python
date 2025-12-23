"""
Practical Scraper Examples
Real-world scraping scenarios for different types of websites
"""

from scraper import WebScraper
from advanced_scraper import AdvancedScraper
import re
from typing import List, Dict, Optional


class ProductScraper(AdvancedScraper):
    """
    Scraper optimized for e-commerce/product pages
    """
    
    def extract_price(self, text: str) -> Optional[float]:
        """
        Extract price from text using regex
        
        Args:
            text: Text containing price
            
        Returns:
            Price as float or None
        """
        # Match common price patterns: $99.99, €99,99, 99.99, etc.
        patterns = [
            r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # $1,234.56
            r'€\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',   # €1.234,56
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*USD', # 1,234.56 USD
            r'(\d+(?:\.\d{2})?)'                        # Simple: 99.99
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                price_str = match.group(1).replace(',', '')
                try:
                    return float(price_str)
                except ValueError:
                    continue
        
        return None
    
    def scrape_product(self, url: str) -> Dict:
        """
        Scrape product information
        
        Args:
            url: Product page URL
            
        Returns:
            Dictionary with product data
        """
        soup = self.fetch_page(url)
        if not soup:
            return {}
        
        product = {
            'url': url,
            'name': '',
            'price': None,
            'description': '',
            'images': [],
            'specifications': {},
            'availability': ''
        }
        
        # Common product name selectors
        name_selectors = ['h1', '.product-title', '#product-name', '[itemprop="name"]']
        for selector in name_selectors:
            name_elem = soup.select_one(selector)
            if name_elem:
                product['name'] = name_elem.get_text(strip=True)
                break
        
        # Common price selectors
        price_selectors = ['.price', '.product-price', '[itemprop="price"]', '.cost']
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                product['price'] = self.extract_price(price_text)
                if product['price']:
                    break
        
        # Description
        desc_selectors = ['.description', '#description', '[itemprop="description"]']
        for selector in desc_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                product['description'] = desc_elem.get_text(strip=True)
                break
        
        # Images
        product['images'] = self.extract_images(soup)
        
        # Specifications (look for key-value pairs)
        spec_table = soup.select_one('.specifications, .specs, .product-details')
        if spec_table:
            for row in spec_table.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                if len(cells) == 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    product['specifications'][key] = value
        
        return product


class BlogScraper(AdvancedScraper):
    """
    Scraper optimized for blog posts
    """
    
    def scrape_blog_post(self, url: str) -> Dict:
        """
        Scrape blog post content
        
        Args:
            url: Blog post URL
            
        Returns:
            Dictionary with blog post data
        """
        soup = self.fetch_page(url)
        if not soup:
            return {}
        
        post = {
            'url': url,
            'title': '',
            'author': '',
            'date': '',
            'categories': [],
            'tags': [],
            'content': '',
            'comments_count': 0
        }
        
        # Title
        title_elem = soup.select_one('h1, .post-title, article h1')
        if title_elem:
            post['title'] = title_elem.get_text(strip=True)
        
        # Author
        author_selectors = ['.author', '.by-author', '[rel="author"]', '.post-author']
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                post['author'] = author_elem.get_text(strip=True)
                break
        
        # Date
        date_elem = soup.select_one('time, .date, .published, [datetime]')
        if date_elem:
            post['date'] = date_elem.get('datetime') or date_elem.get_text(strip=True)
        
        # Categories and tags
        category_elems = soup.select('.category, .categories a')
        post['categories'] = [cat.get_text(strip=True) for cat in category_elems]
        
        tag_elems = soup.select('.tag, .tags a')
        post['tags'] = [tag.get_text(strip=True) for tag in tag_elems]
        
        # Content
        content_elem = soup.select_one('article, .post-content, .entry-content, main')
        if content_elem:
            # Get all paragraphs
            paragraphs = content_elem.find_all('p')
            post['content'] = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
        
        # Comments count
        comments_elem = soup.select_one('.comments-count, .comment-count')
        if comments_elem:
            comments_text = comments_elem.get_text()
            match = re.search(r'(\d+)', comments_text)
            if match:
                post['comments_count'] = int(match.group(1))
        
        return post
    
    def scrape_blog_listing(self, url: str, max_posts: int = 10) -> List[Dict]:
        """
        Scrape blog listing page
        
        Args:
            url: Blog listing page URL
            max_posts: Maximum number of posts to scrape
            
        Returns:
            List of blog post summaries
        """
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        posts = []
        post_elements = soup.select('article, .post, .blog-post')[:max_posts]
        
        for post_elem in post_elements:
            post_data = {}
            
            # Title and link
            title_link = post_elem.select_one('h2 a, h3 a, .post-title a')
            if title_link:
                post_data['title'] = title_link.get_text(strip=True)
                post_data['url'] = title_link.get('href')
                if post_data['url']:
                    post_data['url'] = requests.compat.urljoin(url, post_data['url'])
            
            # Excerpt
            excerpt = post_elem.select_one('.excerpt, .summary, p')
            if excerpt:
                post_data['excerpt'] = excerpt.get_text(strip=True)
            
            # Date
            date_elem = post_elem.select_one('time, .date')
            if date_elem:
                post_data['date'] = date_elem.get('datetime') or date_elem.get_text(strip=True)
            
            if post_data:
                posts.append(post_data)
        
        return posts


class SocialMediaScraper(AdvancedScraper):
    """
    Scraper for publicly accessible social media content
    Note: Respects robots.txt and Terms of Service
    """
    
    def extract_social_post(self, soup, post_selector: str) -> List[Dict]:
        """
        Extract social media posts from a page
        
        Args:
            soup: BeautifulSoup object
            post_selector: CSS selector for post containers
            
        Returns:
            List of post data
        """
        posts = []
        post_elements = soup.select(post_selector)
        
        for post_elem in post_elements:
            post = {
                'text': '',
                'author': '',
                'timestamp': '',
                'likes': 0,
                'shares': 0,
                'comments': 0
            }
            
            # Text content
            text_elem = post_elem.select_one('.post-text, .content, p')
            if text_elem:
                post['text'] = text_elem.get_text(strip=True)
            
            # Author
            author_elem = post_elem.select_one('.author, .username, .user')
            if author_elem:
                post['author'] = author_elem.get_text(strip=True)
            
            # Extract metrics (likes, shares, etc.)
            metrics = post_elem.select('.metric, .stat, .count')
            for metric in metrics:
                text = metric.get_text(strip=True).lower()
                match = re.search(r'(\d+)', text)
                if match:
                    count = int(match.group(1))
                    if 'like' in text:
                        post['likes'] = count
                    elif 'share' in text:
                        post['shares'] = count
                    elif 'comment' in text:
                        post['comments'] = count
            
            posts.append(post)
        
        return posts


def demo_practical_scrapers():
    """
    Demonstrate practical scraping scenarios
    """
    print("=" * 60)
    print("Practical Web Scraping Examples")
    print("=" * 60)
    
    # Example 1: Product scraping pattern
    print("\nExample 1: Product Scraping Structure")
    print("-" * 60)
    
    product_scraper = ProductScraper("http://books.toscrape.com")
    
    # Scrape a sample book page
    soup = product_scraper.fetch_page("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    
    if soup:
        # Extract product details
        title = soup.select_one('h1')
        price = soup.select_one('.price_color')
        availability = soup.select_one('.availability')
        
        print("\nBook Details:")
        print(f"  Title: {title.get_text(strip=True) if title else 'N/A'}")
        print(f"  Price: {price.get_text(strip=True) if price else 'N/A'}")
        print(f"  Availability: {availability.get_text(strip=True) if availability else 'N/A'}")
        
        # Extract product table
        product_info = soup.select_one('.product_page table')
        if product_info:
            print("\n  Product Information:")
            for row in product_info.find_all('tr'):
                cells = row.find_all(['th', 'td'])
                if len(cells) == 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    print(f"    {key}: {value}")
    
    # Example 2: Scraping multiple products from catalog
    print("\n" + "=" * 60)
    print("Example 2: Catalog Scraping")
    print("-" * 60)
    
    catalog_soup = product_scraper.fetch_page("http://books.toscrape.com/")
    if catalog_soup:
        books = catalog_soup.select('article.product_pod')
        print(f"\nFound {len(books)} books on the page")
        
        print("\nFirst 3 books:")
        for i, book in enumerate(books[:3], 1):
            title_elem = book.select_one('h3 a')
            price_elem = book.select_one('.price_color')
            rating_elem = book.select_one('.star-rating')
            
            title = title_elem.get('title') if title_elem else 'N/A'
            price = price_elem.get_text(strip=True) if price_elem else 'N/A'
            rating = rating_elem.get('class')[1] if rating_elem else 'N/A'
            
            print(f"\n  {i}. {title}")
            print(f"     Price: {price}")
            print(f"     Rating: {rating}")
    
    # Example 3: Extract structured data
    print("\n" + "=" * 60)
    print("Example 3: Structured Data Extraction")
    print("-" * 60)
    
    # Extract all books with their details
    if catalog_soup:
        books_data = product_scraper.extract_nested_data(
            catalog_soup,
            'article.product_pod',
            {
                'title': 'h3 a',
                'price': '.price_color',
                'availability': '.availability'
            }
        )
        
        print(f"\nExtracted structured data for {len(books_data)} books")
        if books_data:
            print(f"\nSample book data structure:")
            for key, value in books_data[0].items():
                print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("Practical scraping examples complete!")


if __name__ == "__main__":
    import requests
    demo_practical_scrapers()
