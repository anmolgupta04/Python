"""
Web Scraping Utilities
Helper functions for common scraping challenges
"""

import re
import time
from typing import List, Dict, Optional, Callable
from urllib.parse import urlparse, urljoin
from functools import wraps
import hashlib


def rate_limiter(calls_per_second: float = 1.0):
    """
    Decorator to limit the rate of function calls
    
    Args:
        calls_per_second: Maximum number of calls per second
    """
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator


def retry_on_failure(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator to retry function on failure with exponential backoff
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator


class URLValidator:
    """
    Validate and normalize URLs
    """
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def normalize_url(url: str, base_url: str = None) -> str:
        """
        Normalize URL (remove fragments, handle relative URLs)
        
        Args:
            url: URL to normalize
            base_url: Base URL for resolving relative URLs
            
        Returns:
            Normalized URL
        """
        if base_url:
            url = urljoin(base_url, url)
        
        parsed = urlparse(url)
        # Remove fragment
        normalized = parsed._replace(fragment='').geturl()
        return normalized
    
    @staticmethod
    def get_domain(url: str) -> str:
        """Extract domain from URL"""
        parsed = urlparse(url)
        return parsed.netloc
    
    @staticmethod
    def is_same_domain(url1: str, url2: str) -> bool:
        """Check if two URLs are from the same domain"""
        return URLValidator.get_domain(url1) == URLValidator.get_domain(url2)


class TextCleaner:
    """
    Clean and process scraped text
    """
    
    @staticmethod
    def clean_whitespace(text: str) -> str:
        """Remove extra whitespace and normalize line breaks"""
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text
    
    @staticmethod
    def remove_html_comments(html: str) -> str:
        """Remove HTML comments"""
        return re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """Extract email addresses from text"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """Extract phone numbers from text (US format)"""
        patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (123) 456-7890
            r'\d{3}-\d{3}-\d{4}',                     # 123-456-7890
            r'\d{10}'                                  # 1234567890
        ]
        
        numbers = []
        for pattern in patterns:
            numbers.extend(re.findall(pattern, text))
        return list(set(numbers))  # Remove duplicates
    
    @staticmethod
    def extract_dates(text: str) -> List[str]:
        """Extract dates from text (various formats)"""
        patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',              # 12/31/2023
            r'\d{4}-\d{2}-\d{2}',                    # 2023-12-31
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b'  # January 1, 2023
        ]
        
        dates = []
        for pattern in patterns:
            dates.extend(re.findall(pattern, text, re.IGNORECASE))
        return dates
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
        """Truncate text to maximum length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix


class DataCache:
    """
    Simple in-memory cache for scraped data
    """
    
    def __init__(self):
        self.cache = {}
    
    def _get_key(self, url: str) -> str:
        """Generate cache key from URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def get(self, url: str) -> Optional[Dict]:
        """Get cached data for URL"""
        key = self._get_key(url)
        return self.cache.get(key)
    
    def set(self, url: str, data: Dict):
        """Cache data for URL"""
        key = self._get_key(url)
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def clear(self):
        """Clear all cached data"""
        self.cache.clear()
    
    def is_cached(self, url: str, max_age: float = 3600) -> bool:
        """
        Check if URL is cached and not expired
        
        Args:
            url: URL to check
            max_age: Maximum cache age in seconds
            
        Returns:
            True if cached and not expired
        """
        key = self._get_key(url)
        if key not in self.cache:
            return False
        
        age = time.time() - self.cache[key]['timestamp']
        return age < max_age


class RobotsTxtParser:
    """
    Parse and respect robots.txt
    """
    
    def __init__(self, user_agent: str = '*'):
        self.user_agent = user_agent
        self.rules = {}
    
    def fetch_robots_txt(self, base_url: str) -> str:
        """Fetch robots.txt from domain"""
        import requests
        robots_url = urljoin(base_url, '/robots.txt')
        try:
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                return response.text
        except:
            pass
        return ''
    
    def parse_robots_txt(self, content: str):
        """Parse robots.txt content"""
        current_agent = None
        self.rules = {'*': {'allow': [], 'disallow': []}}
        
        for line in content.split('\n'):
            line = line.split('#')[0].strip()  # Remove comments
            if not line:
                continue
            
            if line.lower().startswith('user-agent:'):
                current_agent = line.split(':', 1)[1].strip()
                if current_agent not in self.rules:
                    self.rules[current_agent] = {'allow': [], 'disallow': []}
            
            elif line.lower().startswith('disallow:'):
                path = line.split(':', 1)[1].strip()
                if current_agent and path:
                    self.rules[current_agent]['disallow'].append(path)
            
            elif line.lower().startswith('allow:'):
                path = line.split(':', 1)[1].strip()
                if current_agent and path:
                    self.rules[current_agent]['allow'].append(path)
    
    def can_fetch(self, url: str) -> bool:
        """
        Check if URL can be fetched according to robots.txt
        
        Args:
            url: URL to check
            
        Returns:
            True if allowed to fetch
        """
        parsed = urlparse(url)
        path = parsed.path or '/'
        
        # Get rules for this user agent, fall back to *
        rules = self.rules.get(self.user_agent, self.rules.get('*', {'allow': [], 'disallow': []}))
        
        # Check disallow rules
        for disallow_path in rules['disallow']:
            if path.startswith(disallow_path):
                # Check if explicitly allowed
                for allow_path in rules['allow']:
                    if path.startswith(allow_path):
                        return True
                return False
        
        return True


def extract_all_text(soup, ignore_tags: List[str] = None) -> str:
    """
    Extract all text from BeautifulSoup object, ignoring specified tags
    
    Args:
        soup: BeautifulSoup object
        ignore_tags: List of tag names to ignore (e.g., ['script', 'style'])
        
    Returns:
        Extracted text
    """
    if ignore_tags:
        for tag in ignore_tags:
            for element in soup.find_all(tag):
                element.decompose()
    
    return soup.get_text(separator=' ', strip=True)


def create_filename_from_url(url: str, extension: str = 'html') -> str:
    """
    Create a safe filename from URL
    
    Args:
        url: URL to convert
        extension: File extension
        
    Returns:
        Safe filename
    """
    parsed = urlparse(url)
    path = parsed.path.strip('/').replace('/', '_')
    
    # Remove special characters
    path = re.sub(r'[^\w\-_]', '_', path)
    
    if not path:
        path = 'index'
    
    return f"{path}.{extension}"


def demo_utilities():
    """
    Demonstrate utility functions
    """
    print("=" * 60)
    print("Web Scraping Utilities Demo")
    print("=" * 60)
    
    # URL Validation
    print("\n1. URL Validation")
    print("-" * 60)
    
    urls = [
        "https://www.example.com/page",
        "not-a-url",
        "ftp://files.example.com/file.txt"
    ]
    
    for url in urls:
        is_valid = URLValidator.is_valid_url(url)
        print(f"  {url}: {'Valid' if is_valid else 'Invalid'}")
    
    # Text Cleaning
    print("\n2. Text Cleaning")
    print("-" * 60)
    
    dirty_text = "  This   has    extra    spaces\n\n\nand   breaks  "
    clean_text = TextCleaner.clean_whitespace(dirty_text)
    print(f"  Original: '{dirty_text}'")
    print(f"  Cleaned: '{clean_text}'")
    
    # Extract emails
    print("\n3. Data Extraction")
    print("-" * 60)
    
    sample_text = "Contact us at support@example.com or sales@example.org. Call 123-456-7890."
    emails = TextCleaner.extract_emails(sample_text)
    phones = TextCleaner.extract_phone_numbers(sample_text)
    
    print(f"  Text: {sample_text}")
    print(f"  Emails found: {emails}")
    print(f"  Phones found: {phones}")
    
    # Caching
    print("\n4. Caching")
    print("-" * 60)
    
    cache = DataCache()
    test_url = "https://example.com/test"
    test_data = {"title": "Test Page", "content": "Sample content"}
    
    print(f"  Cached: {cache.is_cached(test_url)}")
    cache.set(test_url, test_data)
    print(f"  Cached after set: {cache.is_cached(test_url)}")
    retrieved = cache.get(test_url)
    print(f"  Retrieved data: {retrieved['data']}")
    
    # Rate limiting demonstration
    print("\n5. Rate Limiting")
    print("-" * 60)
    
    @rate_limiter(calls_per_second=2.0)
    def limited_function():
        print(f"    Called at {time.time():.2f}")
    
    print("  Calling function 4 times (limited to 2 calls/second):")
    for i in range(4):
        limited_function()
    
    print("\n" + "=" * 60)
    print("Utilities demo complete!")


if __name__ == "__main__":
    demo_utilities()
