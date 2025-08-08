import os
from my_logging import getLogger
from playwright_utils import playwright_page, BASE_URL, DATA_DIR
from playwright.sync_api import sync_playwright, expect
from basetestcase import BaseTestCase
from utils.page_locator import PageLocator

import pandas
import unittest

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))

class TestTable(BaseTestCase):
    def setUp(self):
        self.file_name = 'dummy_data_various_types.parquet'
        self.file_path = os.path.join(DATA_DIR, self.file_name)
        self.df = pandas.read_parquet(self.file_path)
        self.table_url = f"{BASE_URL}/Table?filePath={self.file_path}"


    def test_render_table(self):
        """Test that the table renders"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)

            pl.sql_status_count_running_0().wait_for(state='visible')

            for tab in ['MainTable', 'HeatMap', 'Histogram', 'BoxPlot', 'BubblePlot']:
                tab_button = pl.tab_panel_header(tab)
                self.assertTrue(tab_button.is_visible(), f"Tab button for {tab} is not visible")
                self.assertEqual(tab_button.inner_text(), tab)
            logger.info('Tabs are rendered')

            # Check that the column headers are rendered
            df = pandas.read_parquet(os.path.join(DATA_DIR, self.file_name))
            for c in df.columns:
                column_header = pl.table_header(c)
                self.assertEqual(column_header.inner_text(), c)
            logger.info('Column headers are rendered')



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
            x_before = pl.get_relative_x_of_column(column)
            logger.info(f"Column {column} x before sorting: {x_before}")
            # Get the sibling column header
            # Get the parent element that contains the column header
            sort_button = column_header.locator("xpath=..").locator(f"[data-ref=eLabel]")
            self.assertTrue(self.is_element_in_view(table, sort_button), "Sort button should be visible")
            sort_button.click()
            self.assertTrue(self.is_element_in_view(table, sort_button), "Sort button should stay visible after clicking")
            x_after = pl.get_relative_x_of_column(column)
            logger.info(f"Column {column} x after sorting: {x_after}")
            self.assertEqual(x_after, x_before, f"Column header after sorting should be at the same position")


    def test_column_navigation(self):
        """Test that the column navigation works"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)


            for col in ['one_value_string', 'uint64', 'halffloat', 'bool_with_nulls', 'struct.y']:
                nav_button = pl.column_navigation_button(col)
                self.assertIsNotNone(nav_button, f"Column navigation button for {col} is not found")
                x_before = pl.get_relative_x_of_column(col)
                logger.info(f"Column {col} x before navigation: {x_before}")
                nav_button.click()
                page.wait_for_timeout(300)
                x_after = pl.get_relative_x_of_column(col)
                logger.info(f"Column {col} x after navigation: {x_after}")

                self.assertTrue(x_after > 0 and x_after < 30, f"Column header x after navigation is not within 30px of the table: {x_after} for {col}")






if __name__ == '__main__':
    unittest.main()


