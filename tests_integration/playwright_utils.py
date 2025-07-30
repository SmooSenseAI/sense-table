from playwright.sync_api import sync_playwright
from contextlib import contextmanager
import logging
from os.path import dirname, abspath
import os
logger = logging.getLogger(__name__)


BASE_URL = f"http://localhost:8000{os.getenv('URL_PREFIX', '')}"
DATA_DIR = os.path.join(dirname(dirname(abspath(__file__))), 'data')

@contextmanager
def playwright_page(headless=True, browser_type='chromium', **browser_options):
    """
    Context manager for Playwright that handles browser lifecycle.
    
    Args:
        headless (bool): Whether to run browser in headless mode
        browser_type (str): Browser type ('chromium', 'firefox', 'webkit')
        **browser_options: Additional browser launch options
    
    Yields:
        Page: Playwright page object
    
    Example:
        with playwright_page(headless=True) as page:
            page.goto("https://example.com")
            # Your test code here
    """
    with sync_playwright() as p:
        # Get the browser launcher based on type
        browser_launcher = getattr(p, browser_type)
        
        # Launch browser with options
        browser = browser_launcher.launch(headless=headless, **browser_options)
        
        try:
            # Create new page
            page = browser.new_page()
            logger.debug(f"Browser launched ({browser_type}, headless={headless})")
            
            yield page
            
        finally:
            # Always close browser, even if an exception occurs
            browser.close()
            logger.debug("Browser closed")


@contextmanager
def playwright_browser(headless=True, browser_type='chromium', **browser_options):
    """
    Context manager for Playwright that yields the browser object instead of page.
    Useful when you need to create multiple pages or have more control.
    
    Args:
        headless (bool): Whether to run browser in headless mode
        browser_type (str): Browser type ('chromium', 'firefox', 'webkit')
        **browser_options: Additional browser launch options
    
    Yields:
        Browser: Playwright browser object
    
    Example:
        with playwright_browser(headless=True) as browser:
            page1 = browser.new_page()
            page2 = browser.new_page()
            # Your test code here
    """
    with sync_playwright() as p:
        # Get the browser launcher based on type
        browser_launcher = getattr(p, browser_type)
        
        # Launch browser with options
        browser = browser_launcher.launch(headless=headless, **browser_options)
        
        try:
            logger.debug(f"Browser launched ({browser_type}, headless={headless})")
            yield browser
            
        finally:
            # Always close browser, even if an exception occurs
            browser.close()
            logger.debug("Browser closed")


class PlaywrightTestMixin:
    """
    Mixin class that provides convenient methods for Playwright testing.
    Can be used with unittest.TestCase or other test frameworks.
    """
    
    def screenshot(self, page, name="screenshot"):
        """
        Take a screenshot and save it with a descriptive name.
        
        Args:
            page: Playwright page object
            name (str): Name for the screenshot file
        """
        import os
        
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Generate filename with test method name if available
        test_name = getattr(self, '_testMethodName', 'test')
        filename = f"{test_name}_{name}.png"
        filepath = os.path.join(screenshots_dir, filename)
        
        # Take screenshot
        page.screenshot(path=filepath, full_page=True)
        logger.info(f"Screenshot saved: {filepath}")
    
    def wait_for_url_contains(self, page, url_fragment, timeout=5000):
        """
        Wait for URL to contain a specific fragment.
        
        Args:
            page: Playwright page object
            url_fragment (str): Fragment that should be in the URL
            timeout (int): Timeout in milliseconds
        """
        page.wait_for_url(f"**/{url_fragment}", timeout=timeout)
        logger.info(f"URL contains '{url_fragment}': {page.url}")
    
    def assert_page_title_contains(self, page, title_fragment):
        """
        Assert that page title contains a specific fragment.
        
        Args:
            page: Playwright page object
            title_fragment (str): Fragment that should be in the title
        """
        title = page.title()
        assert title_fragment in title, f"Title '{title}' does not contain '{title_fragment}'"
        logger.info(f"Page title contains '{title_fragment}': {title}") 


    def is_element_in_view(self, container, element):
        container_box = container.bounding_box()
        element_box = element.bounding_box()

        if not container_box or not element_box:
            return False

        return (
            container_box["x"] <= element_box["x"] <= container_box["x"] + container_box["width"]
            and container_box["y"] <= element_box["y"] <= container_box["y"] + container_box["height"]
        )