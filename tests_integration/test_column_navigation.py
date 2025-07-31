import os
from my_logging import getLogger
from playwright_utils import playwright_page, BASE_URL, DATA_DIR
from playwright.sync_api import sync_playwright, expect
from basetestcase import BaseTableTestCase
import pandas
from basetestcase import PageLocator
import unittest

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))

class TestColumnNavigation(BaseTableTestCase):

    def test_column_navigation(self):
        """Test that the column navigation works"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)

            table = pl.table_root()

            def get_relative_x(element):
                return element.bounding_box()['x'] - table.bounding_box()['x']

            def check_column(_col: str):
                nav_button = pl.column_navigation_button(_col)
                self.assertIsNotNone(nav_button, f"Column navigation button for {_col} is not found")
                column_header = pl.table_header(_col)
                self.assertIsNotNone(column_header, f"Column header for {_col} is not found")
                logger.info(f"Column {_col} x before navigation: {get_relative_x(column_header)}")
                nav_button.click()
                page.wait_for_timeout(300)
                column_header_now = pl.table_header(_col)
                rel_x_after = get_relative_x(column_header_now)
                logger.info(f"Column {_col} x after navigation: {rel_x_after}")

                self.assertTrue(rel_x_after > 0 and rel_x_after < 30, f"Column header x after navigation is not within 30px of the table: {rel_x_after} for {_col}")


            for col in ['one_value_string', 'uint64', 'halffloat', 'bool_with_nulls', 'struct.y']:
                check_column(col)









if __name__ == '__main__':
    unittest.main()


