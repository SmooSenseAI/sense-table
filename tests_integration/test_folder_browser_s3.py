import os
import unittest

from basetestcase import BaseTestCase
from my_logging import getLogger
from playwright.sync_api import expect
from playwright_utils import BASE_URL, playwright_page
from utils.page_locator import PageLocator

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))


class TestFolderBrowser(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.root_folder = "s3://sense-table-demo/datasets"
        self.folder_browser_url = f"{BASE_URL}/FolderBrowser?rootFolder={self.root_folder}"
        logger.info(f"Testing with folder browser URL: {self.folder_browser_url}")

    def test_readme_file(self):
        with playwright_page(headless=True) as page:
            # Navigate to the home page first
            page.goto(self.folder_browser_url)
            self.assertEqual(
                page.locator("div.wmde-markdown").count(), 0, "No readme.md file should be present"
            )
            logger.info("No readme.md file and markdown display at the beginning")

            pl = PageLocator(page)

            readme = page.locator("div.wmde-markdown")
            readme.wait_for(state="visible")
            content_text = readme.inner_text()
            self.assertTrue("Datasets" in content_text, "Readme content be rendered")

            ## Update readme again
            pl.locate_and_wait("div#readme-editor-trigger").click()
            card = pl.locate_and_wait("div#readme-editor-card")
            content = card.locator("div.cm-content")
            content.clear()
            new_content = "Updated content again"
            content.type(new_content)
            card.locator('button:has-text("Save")').click()

            expect(page.locator("div.toast")).to_have_text("FORBIDDEN | Contact admin for access")


if __name__ == "__main__":
    unittest.main()
