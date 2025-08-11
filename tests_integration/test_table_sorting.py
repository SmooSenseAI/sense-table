import os
from my_logging import getLogger
from playwright_utils import playwright_page, DATA_DIR
from basetestcase import BaseTableTestCase
from utils.page_locator import PageLocator

import pandas
import unittest

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))

class TestTableSorting(BaseTableTestCase):

    def test_horizontal_scroll_after_sorting(self):
        """Test that the main table has horizontal scroll"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)
            table = pl.table_root()

            column = 'halffloat'
            column_header = pl.table_header(column)
            self.assertFalse(self.is_element_in_view(table, column_header), f"Column header {column} is initially not in view")

            column_header.scroll_into_view_if_needed()
            self.assertTrue(self.is_element_in_view(table, column_header), f"Column header {column} should be in view after scrolling")
            x_before = pl.get_relative_x_of_column(column)
            logger.info(f"Column {column} x before sorting: {x_before}")
            sort_button = pl.table_header_sort_button(column)
            self.assertTrue(self.is_element_in_view(table, sort_button), "Sort button should be visible")
            sort_button.click()
            page.wait_for_timeout(500)
            self.assertTrue(self.is_element_in_view(table, sort_button), "Sort button should stay visible after clicking")
            x_after = pl.get_relative_x_of_column(column)
            logger.info(f"Column {column} x after sorting: {x_after}")
            self.assertEqual(x_after, x_before, f"Column header after sorting should be at the same position")
            values = pl.column_cell_values(column)
            logger.info(f"Column {column} values: {values}")

    def test_sorting(self):
        """Test that the table sorts"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)
            column = 'idx_int'
            sort_button = pl.table_header_sort_button(column)

            # First sort ascending
            sort_button.click()
            values = pl.column_cell_values(column)
            page.wait_for_timeout(500)
            expected = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            self.assertListEqual(values, expected, f"Column {column} values should be sorted in ascending order")

            # Then sort descending
            sort_button.click()
            page.wait_for_timeout(500)
            values = pl.column_cell_values(column)
            expected = ['199', '198', '197', '196', '195', '194', '193', '192', '191', '190']
            self.assertListEqual(values, expected, f"Column {column} values should be sorted in descending order")



if __name__ == '__main__':
    unittest.main()


