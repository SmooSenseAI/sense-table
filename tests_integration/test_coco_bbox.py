import os
from my_logging import getLogger
from playwright_utils import playwright_page, BASE_URL, DATA_DIR
from playwright.sync_api import sync_playwright, expect
from basetestcase import BaseTestCase, PageLocator
import pandas
import unittest
import pathlib
import shutil

logger = getLogger(__name__)

PWD = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(PWD, '../docs/public/images/coco')

class TestCocoBboxTable(BaseTestCase):
    def setUp(self):
        self.file_path = 's3://sense-table-demo/datasets/COCO2017/bbox.parquet'
        self.table_url = f"{BASE_URL}/Table?filePath={self.file_path}"
        shutil.rmtree(SCREENSHOT_DIR, ignore_errors=True)
        pathlib.Path(SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)

    def do_column_stats(self, color_mode: str):
        """Test that the table renders"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page

            page.goto(self.table_url)
            pl = PageLocator(page)
            if color_mode == 'light':
                pl.icon_color_mode().click()

            page.wait_for_load_state('networkidle')
            pl.select_column('galleryCaptionColumn', 'category_name')

            page.locator('.cell-image_id').nth(0).click()
            page.wait_for_load_state('networkidle')

            page.screenshot(path=f"{SCREENSHOT_DIR}/all_{color_mode}.jpg")


            for column in ['category_name', 'bbox_width']:
                stats_cell = pl.column_stats_cell(column)
                stats_cell.screenshot(path=f"{SCREENSHOT_DIR}/column_stats_cell_{column}_{color_mode}.jpg")
                stats_cell.click()
                stats_card = pl.column_stats_card(column)
                stats_card.screenshot(path=f"{SCREENSHOT_DIR}/column_stats_card_{column}_{color_mode}.jpg")
                stats_card.locator('.btn-close').click()

    def test_column_stats(self):
        self.do_column_stats('light')
        self.do_column_stats('dark')



if __name__ == '__main__':
    unittest.main()


