import os
from my_logging import getLogger
from playwright_utils import playwright_page, DATA_DIR
from basetestcase import BaseTableTestCase
from utils.page_locator import PageLocator

import pandas
import unittest

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))

class TestTableFiltering(BaseTableTestCase):

    def apply_enum_filter(self, page, column: str, value: str):
        pl = PageLocator(page)
        pl.column_stats_cell(column).click()
        card = pl.column_stats_card(column)
        card.scroll_into_view_if_needed()
        card.wait_for(state='visible')

        card.locator(f'text:has-text("{value}")').click()
        card.locator('button:has-text("Apply filters")').click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(500)

    def apply_range_filter(self, page, column: str, min_value: str, max_value: str):
        pl = PageLocator(page)
        pl.column_stats_cell(column).click()
        card = pl.column_stats_card(column)
        card.scroll_into_view_if_needed()
        card.wait_for(state='visible')
        input_min = card.locator('input').first
        input_min.fill(min_value)
        input_max = card.locator('input').last
        input_max.fill(max_value)
        card.locator('button:has-text("Apply filters")').click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(500)

    def apply_text_filter(self, page, column: str, value: str):
        pl = PageLocator(page)
        input = pl.column_stats_cell(column).locator('input')
        input.fill(value)
        input.press('Enter')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(500)

    def assert_filter_count(self, page, count: int):
        pl = PageLocator(page)
        pl.border_panel_header('Filters').click()
        page.locator(f'h6:has-text("Column Filters: {count}")').wait_for(state='visible')

    def test_filtering_boolean(self):
        column = 'bool_with_nulls'
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            self.apply_enum_filter(page, column, 'true')
            self.assert_filter_count(page, 1)

    def test_filtering_enum(self):
        column = 'string_with_nulls'
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)
            self.apply_enum_filter(page, column, 'emoji')

            for value in pl.column_cell_values(column):
                self.assertEqual(value, 'emoji 🤣')
            self.assert_filter_count(page, 1)

    def test_filtering_range(self):
        column = 'idx_int'
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)
            self.apply_range_filter(page, column, '20', '30')
            for value in pl.column_cell_values(column):
                v = int(value)
                self.assertTrue(20 <= v <= 30, f"Value {v} is not in range 20-30")
            self.assert_filter_count(page, 1)

    def test_filtering_text(self):
        column = 'idx_str'
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)
            self.apply_text_filter(page, column, 's5')
            for value in pl.column_cell_values(column):
                self.assertTrue('s5' in value, f"Value {value} should contain 's5'")
            self.assert_filter_count(page, 1)

    def test_filtering_multiple(self):
        with playwright_page(headless=True) as page:
            page.goto(self.table_url)
            pl = PageLocator(page)
            self.apply_text_filter(page, 'idx_str', 's5')
            self.apply_range_filter(page, 'idx_int', '50', '60')
            self.apply_enum_filter(page, 'bool_with_nulls', 'true')
            self.assert_filter_count(page, 3)



if __name__ == '__main__':
    unittest.main()


