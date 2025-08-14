import os
import unittest

from basetestcase import BaseTableTestCase
from my_logging import getLogger
from playwright_utils import playwright_page
from utils.page_locator import PageLocator

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))


class TestTable(BaseTableTestCase):
    def test_render_table(self):
        """Test that the table renders"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)

            pl.sql_status_count_running_0().wait_for(state="visible")

            for tab in ["MainTable", "HeatMap", "Histogram", "BoxPlot", "BubblePlot"]:
                tab_button = pl.tab_panel_header(tab)
                self.assertTrue(tab_button.is_visible(), f"Tab button for {tab} is not visible")
                self.assertEqual(tab_button.inner_text(), tab)
            logger.info("Tabs are rendered")

            # Check that the column headers are rendered
            for c in self.df.columns:
                column_header = pl.table_header(c)
                self.assertEqual(column_header.inner_text(), c)
            logger.info("Column headers are rendered")

    def test_render_only_main_table(self):
        """Test that the table renders"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url.replace("/Table", "/MainTable"))
            pl = PageLocator(page)

            pl.sql_status_count_running_0().wait_for(state="visible")

            # Check that the column headers are rendered
            for c in self.df.columns:
                column_header = pl.table_header(c)
                self.assertEqual(column_header.inner_text(), c)
            logger.info("Column headers are rendered")

    def test_column_navigation(self):
        """Test that the column navigation works"""
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.table_url)
            pl = PageLocator(page)

            for col in ["one_value_string", "uint64", "halffloat", "bool_with_nulls", "struct.y"]:
                nav_button = pl.column_navigation_button(col)
                self.assertIsNotNone(nav_button, f"Column navigation button for {col} is not found")
                x_before = pl.get_relative_x_of_column(col)
                logger.info(f"Column {col} x before navigation: {x_before}")
                nav_button.click()
                page.wait_for_timeout(300)
                x_after = pl.get_relative_x_of_column(col)
                logger.info(f"Column {col} x after navigation: {x_after}")

                self.assertTrue(
                    x_after > 0 and x_after < 30,
                    f"Column header x after navigation is not within 30px of the table: {x_after} for {col}",
                )


if __name__ == "__main__":
    unittest.main()
