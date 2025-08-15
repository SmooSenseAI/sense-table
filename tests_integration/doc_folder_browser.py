import os
import unittest

from basetestcase import BaseTestCase
from my_logging import getLogger
from playwright_utils import BASE_URL, playwright_page
from utils.page_locator import PageLocator
from utils.screen_taker import ScreenTaker

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))

class TestFolderBrowserForDoc(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = f"{BASE_URL}/FolderBrowser?rootFolder=s3://sense-table-demo/datasets"

    def test_markdown_readme(self):
        url = f"{BASE_URL}/FolderBrowser?rootFolder=s3://sense-table-demo"

        with playwright_page(headless=False) as page:
            page.goto(url)
            pl = PageLocator(page)
            page.wait_for_load_state('networkidle')
            st = ScreenTaker(page, 'folder_browser')
            pl.folder_nav_item('PreviewFiles').click()
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(500)

            def pre_actions():
                page.locator('#readme-editor-trigger').click()
                page.wait_for_timeout(500)
            def post_actions():
                page.locator('.MuiCardHeader-action >> .btn-close').click()
                page.wait_for_timeout(500)

            st.take(page, 'markdown_readme', pre_actions, post_actions)

    def test_preview_folder(self):
        with playwright_page(headless=False) as page:
            page.goto(self.url)
            page.wait_for_load_state('networkidle')
            st = ScreenTaker(page, 'folder_browser')
            page.wait_for_load_state('networkidle')
            st.take(page, 'preview_folder')

    def test_preview_json(self):
        with playwright_page(headless=False) as page:
            page.goto(self.url)
            pl = PageLocator(page)
            page.wait_for_load_state('networkidle')
            st = ScreenTaker(page, 'folder_browser')
            pl.folder_nav_item('COCO2017').click()
            page.wait_for_load_state('networkidle')

            json_file = page.locator("div.folder-list-item:has-text('captions_val2017.json')")
            json_file.hover()
            json_file.click()
            page.wait_for_load_state('networkidle')
            pl.locate_and_wait('button#json-expand-more').click()
            st.take(page, 'preview_json')

    def test_preview_parquet(self):
        with playwright_page(headless=False) as page:
            page.goto(self.url)
            pl = PageLocator(page)
            page.wait_for_load_state('networkidle')
            st = ScreenTaker(page, 'folder_browser')
            pl.folder_nav_item('ClickBench-100M.parquet').click()
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            st.take(page, 'preview_parquet')

    def test_preview_csv(self):
        with playwright_page(headless=False) as page:
            page.goto(self.url)
            pl = PageLocator(page)
            page.wait_for_load_state('networkidle')
            st = ScreenTaker(page, 'folder_browser')
            pl.folder_nav_item('OpenVid').dblclick()
            page.wait_for_load_state('networkidle')
            pl.folder_nav_item('OpenVid-1M.csv').click()
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(5000)
            st.take(page, 'preview_csv')


    def test_preview_images(self):
        with playwright_page(headless=False) as page:
            page.goto(self.url)
            pl = PageLocator(page)
            page.wait_for_load_state('networkidle')
            st = ScreenTaker(page, 'folder_browser')
            pl.folder_nav_item('Oxford Flowers 102').click()
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(1000)
            st.take(page, 'preview_images')


if __name__ == '__main__':
    unittest.main()


