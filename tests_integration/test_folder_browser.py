import os
from my_logging import getLogger
from playwright_utils import playwright_page, BASE_URL, DATA_DIR
from basetestcase import BaseTestCase
import unittest
logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))

class TestFolderBrowser(BaseTestCase):

    def setUp(self):
        self.root_folder_name = os.path.basename(DATA_DIR)
        self.folder_browser_url = f"{BASE_URL}/FolderBrowser?rootFolder={DATA_DIR}"
        logger.info(f"Testing with folder browser URL: {self.folder_browser_url}")

    def test_homepage_redirect_to_folder_browser(self):
        """Test that the homepage redirects to FolderBrowser after JavaScript execution"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(BASE_URL)

            # Wait for the JavaScript redirect to complete
            self.wait_for_url_contains(page, "FolderBrowser")

            # Check that we got redirected to FolderBrowser
            self.assertIn("FolderBrowser", page.url)


    def test_loading_given_folder(self):
        """Test that the folder browser loads a given folder"""

        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.folder_browser_url)
            self.assert_page_title_contains(page, self.root_folder_name)

            # Find all breadcrumb items with text 'data'
            data_breadcrumbs = page.locator(f"li.MuiBreadcrumbs-li:has-text('{self.root_folder_name}')")
            for b in data_breadcrumbs.all():
                logger.info(f"Breadcrumb: |{b.inner_text()}| |{self.root_folder_name}|")

            # Verify there are exactly 2 breadcrumb items with 'data'
            count = data_breadcrumbs.count()
            self.assertEqual(count, 2, f"Expected 2 breadcrumb items with text '{self.root_folder_name}', found {count}")

    def test_preview_parquet_file(self):
        """Test that the folder browser can preview a parquet file"""

        file_name = 'dummy_data_various_types.parquet'

        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.folder_browser_url)
            file_item = page.locator(f"div.MuiTreeItem-label:has-text('{file_name}')")
            file_item.click()
            # Wait for the parquet preview table to appear
            page.wait_for_selector("div.ag-root-wrapper", timeout=5000)

            self.screenshot(page, file_name)

            # Assert showing the parquet preview
            for c in ['column_name', 'column_type', 'cntNull', 'min', 'max']:
                header_cell = page.locator(f"span.ag-header-cell-text:text-is('{c}')")
                self.assertTrue(header_cell.is_visible(), f"Header cell for column '{c}' is not visible")
                self.assertEqual(header_cell.text_content(), c)

    def test_preview_csv_file(self):
        """Test that the folder browser can preview a csv file"""

        file_name = 'dummy_data_various_types.csv'

        with playwright_page(headless=True) as page:
            # Navigate to the home page first
            page.goto(self.folder_browser_url)

            # Set dark theme in local storage after page loads
            page.evaluate("() => { localStorage.setItem('theme', 'dark'); }")

            def check_details(mode: str):
                file_item = page.locator(f"div.MuiTreeItem-label:has-text('{file_name}')")
                file_item.click()
                # Wait for the csv preview table to appear
                page.wait_for_selector("div.ag-root-wrapper", timeout=5000)

                self.screenshot(page, file_name + f"_{mode}")

                # Assert showing the columns from csv
                for c in ['idx_int', 'idx_str', 'pa_null', 'int8']:
                    header_cell = page.locator(f"span.ag-header-cell-text:text-is('{c}')")
                    header_cell.scroll_into_view_if_needed()
                    self.assertTrue(header_cell.is_visible(), f"Header cell for column '{c}' is not visible")
                    self.assertEqual(header_cell.text_content(), c)

            check_details('dark')
            page.locator('#icon-button-color-mode').click()
            check_details('light')

if __name__ == '__main__':
    unittest.main()


