import os
from my_logging import getLogger
from playwright_utils import playwright_page, BASE_URL, DATA_DIR
from playwright.sync_api import sync_playwright, expect
from basetestcase import BaseTestCase, PageLocator, ScreenTaker
import pandas
import unittest

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))

class TestTableForDoc(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.file_name = 'yolov7-object-detection.parquet'
        self.url = f"{BASE_URL}/Table?filePath={os.path.join(DATA_DIR, self.file_name)}"
        logger.info(f"Table URL: {self.url}")

    @unittest.skip("This is for local generation")
    def test_render_table(self):
        with playwright_page(headless=False) as page:
            # Navigate to the home page
            page.goto(self.url)
            page.wait_for_load_state('networkidle')
            pl = PageLocator(page)
            table = pl.table_root()
            page.wait_for_selector("#sql-status-count-running:has-text('0')", timeout=30_000)
            cell = page.locator('div.ag-cell[col-id="category_name"]').last
            cell.scroll_into_view_if_needed()
            cell.click()

            bbox_viz = page.locator('.row-details-field-header:has-text("bbox_viz")')

            bbox_viz.scroll_into_view_if_needed()
            bbox_viz.wait_for(state='visible')
            page.wait_for_timeout(500)

            st = ScreenTaker(page, 'table')

            def pre_actions():
                cell.click()

            st.take(page, 'overview', pre_actions)

    def test_header_stats(self):
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.url)
            page.wait_for_load_state('networkidle')
            pl = PageLocator(page)
            st = ScreenTaker(page, 'table')
            for column in ['category_name', 'iou', 'confidence', 'match_type', 'filename']:
                stats_cell = pl.column_stats_cell(column)
                st.take(stats_cell, f'header_stats_{column}')


    def test_header_stats_card(self):
        with playwright_page(headless=True) as page:
            page.goto(self.url)
            page.wait_for_load_state('networkidle')
            pl = PageLocator(page)
            st = ScreenTaker(page, 'table')
            for column in ['category_name', 'confidence']:
                selector = f"#column-stats-card-{column}"
                def pre_actions():
                    pl.column_navigation_button(column).click()
                    pl.column_stats_cell(column).click()
                    page.locator(selector).scroll_into_view_if_needed()
                    page.wait_for_timeout(1000)

                def post_actions():
                    page.locator(selector).locator('.btn-close').click()

                st.take(page, f'header_stats_card_{column}', pre_actions, post_actions)


if __name__ == '__main__':
    unittest.main()


