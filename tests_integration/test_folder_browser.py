import os
import unittest

from basetestcase import BaseTestCase
from my_logging import getLogger
from playwright.sync_api import TimeoutError, expect
from playwright_utils import BASE_URL, DATA_DIR, playwright_page
from utils.page_locator import PageLocator

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))


class TestFolderBrowser(BaseTestCase):
    def setUp(self):
        super().setUp()
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
            data_breadcrumbs = page.locator(
                f"li.MuiBreadcrumbs-li:has-text('{self.root_folder_name}')"
            )
            # Verify there are exactly 2 breadcrumb items with 'data'
            count = data_breadcrumbs.count()

            self.assertEqual(
                count,
                2,
                f"Expected 2 breadcrumb items with text '{self.root_folder_name}', found {count}",
            )

            btn_copy = page.locator("button#button-copy-to-clipboard")
            btn_copy.click()
            # Verify clipboard content
            clipboard_content = page.evaluate("() => navigator.clipboard.readText()")
            self.assertEqual(clipboard_content, DATA_DIR, "Clipboard content should match DATA_DIR")

    def test_preview_parquet_file(self):
        """Test that the folder browser can preview a parquet file"""

        file_name = "dummy_data_various_types.parquet"

        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.folder_browser_url)
            pl = PageLocator(page)
            pl.folder_nav_item(file_name).click()
            # Wait for the parquet preview table to appear
            pl.table_root()

            for c in ["column_name", "column_type", "cntNull", "min", "max"]:
                header_cell = pl.table_header(c)
                self.assertTrue(
                    header_cell.is_visible(), f"Header cell for column '{c}' is not visible"
                )
                self.assertEqual(header_cell.inner_text(), c)

    def test_preview_csv_file(self):
        """Test that the folder browser can preview a csv file"""

        file_name = "dummy_data_various_types.csv"

        with playwright_page(headless=True) as page:
            # Navigate to the home page first
            page.goto(self.folder_browser_url)
            pl = PageLocator(page)

            pl.folder_nav_item(file_name).click()
            # Wait for the csv preview table to appear
            pl.table_root()

            # Assert showing the columns from csv
            for c in ["idx_int", "idx_str", "pa_null", "int8"]:
                header_cell = pl.table_header(c)
                self.assertTrue(
                    header_cell.is_visible(), f"Header cell for column '{c}' is not visible"
                )
                self.assertEqual(header_cell.inner_text(), c)

    def test_readme_file(self):
        # Ensure there is no readme.md file at the beginning of the test
        readme_path = os.path.join(DATA_DIR, "readme.md")
        if os.path.exists(readme_path):
            os.remove(readme_path)

        # Wait a bit for file system to settle
        import time

        time.sleep(0.1)

        with playwright_page(headless=True) as page:
            # Navigate to the home page first
            page.goto(self.folder_browser_url)
            page.wait_for_load_state("networkidle")  # Wait for all network activity to finish
            self.assertEqual(
                page.locator("div.wmde-markdown").count(), 0, "No readme.md file should be present"
            )
            logger.info("No readme.md file and markdown display at the beginning")

            pl = PageLocator(page)

            # Write readme content
            pl.locate_and_wait("div#readme-editor-trigger").click()
            card = pl.locate_and_wait("div#readme-editor-card")
            self.assertTrue(card.is_visible(), "Readme editor card is not visible")
            content = card.locator("div.cm-content")
            content.click()  # Ensure focus
            page.wait_for_timeout(200)  # Small delay for editor to be ready
            content.type(
                "# Test Readme\nThis is a test readme file with some **markdown** formatting.\n\n- Bullet point 1\n- Bullet point 2"
            )
            page.wait_for_timeout(300)  # Wait for typing to complete
            card.locator('button:has-text("Save")').click()

            # Wait for save to complete and card to hide
            card.wait_for(state="hidden", timeout=5000)
            page.wait_for_load_state("networkidle")  # Wait for save request to complete

            # Sometimes the page needs to refresh to show the markdown
            # Check if markdown content appears, if not refresh the page
            readme = page.locator("div.wmde-markdown")

            # Try waiting for content to appear
            try:
                page.wait_for_selector("div.wmde-markdown:has-text('Test Readme')", timeout=3000)
            except TimeoutError:
                logger.info("Markdown content not visible, refreshing page...")
                page.reload()
                page.wait_for_load_state("networkidle")
                page.wait_for_selector("div.wmde-markdown:has-text('Test Readme')", timeout=5000)

            content_text = readme.inner_text()
            self.assertTrue(
                "This is a test readme file with" in content_text,
                "Readme content should be rendered",
            )
            logger.info("Readme updated now")

            ## Update readme again
            pl.locate_and_wait("div#readme-editor-trigger").click()
            card = pl.locate_and_wait("div#readme-editor-card")
            content = card.locator("div.cm-content")

            # Clear content more reliably
            content.click()
            page.keyboard.press("Control+a")  # Select all
            page.wait_for_timeout(100)

            new_content = "Updated content again"
            content.type(new_content)
            page.wait_for_timeout(300)  # Wait for typing to complete
            card.locator('button:has-text("Save")').click()

            # Wait for save and UI update
            card.wait_for(state="hidden", timeout=5000)
            page.wait_for_load_state("networkidle")

            # Wait specifically for the new content to appear
            page.wait_for_selector(f"div.wmde-markdown:has-text('{new_content}')", timeout=5000)

            # More robust content check
            expect(readme).to_contain_text(new_content, timeout=5000)
            logger.info(f"Readme updated to {new_content}")


if __name__ == "__main__":
    unittest.main()
