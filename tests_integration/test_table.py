import os
from my_logging import getLogger
from playwright_utils import playwright_page, BASE_URL, DATA_DIR
from playwright.sync_api import sync_playwright, expect
from basetestcase import BaseTableTestCase, PageLocator
import pandas
import unittest

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))

class TestTable(BaseTableTestCase):

    def test_render_table(self):
        """Test that the table renders"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)

            # Set dark theme in local storage after page loads
            page.evaluate("() => { localStorage.setItem('theme', 'dark'); }")

            def check_details(mode: str):
                table = pl.table_root()
                page.wait_for_selector("#sql-status-count-running:has-text('0')", timeout=30_000)
                self.screenshot(page, f"table_{mode}")

                for tab in ['MainTable', 'ColumnNavigation', 'Gallery', 'RowDetails', 'HeatMap', 'Histogram', 'BoxPlot', 'BubblePlot']:
                    tab_button = page.locator(f"div.flexlayout__tab_button:has-text('{tab}')")
                    self.assertTrue(tab_button.is_visible(), f"Tab button for {tab} is not visible")
                    self.assertEqual(tab_button.inner_text(), tab)

                # Check that the column headers are rendered
                df = pandas.read_parquet(os.path.join(DATA_DIR, self.file_name))
                for c in df.columns:
                    column_header = pl.table_header(c)
                    self.assertEqual(column_header.inner_text(), c)

            check_details('dark')
            page.locator('#icon-button-color-mode').click()
            check_details('light')


    def test_main_table_horizontal_scroll(self):
        """Test that the main table has horizontal scroll"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)
            table = pl.table_root()

            column = 'halffloat'
            column_header = pl.table_header(column)
            self.assertIsNotNone(column_header, f"Column header {column} is not found")
            self.assertFalse(self.is_element_in_view(table, column_header), f"Column header {column} is initially not in view")

            column_header.scroll_into_view_if_needed()
            self.assertTrue(self.is_element_in_view(table, column_header), f"Column header {column} should be in view after scrolling")
            # Get the sibling column header
            # Get the parent element that contains the column header
            sort_button = column_header.locator("xpath=..").locator(f"[data-ref=eLabel]")
            self.assertTrue(self.is_element_in_view(table, sort_button), "Sort button should be visible")
            sort_button.click()
            self.assertTrue(self.is_element_in_view(table, sort_button), "Sort button should stay visible after clicking")





if __name__ == '__main__':
    unittest.main()


