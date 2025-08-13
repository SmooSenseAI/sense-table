import os
from my_logging import getLogger
from playwright_utils import playwright_page, DATA_DIR, BASE_URL
from basetestcase import BaseTestCase
from utils.page_locator import PageLocator

import pandas
import unittest

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))

class TestSharing(BaseTestCase):
    def setUp(self):
            super().setUp()
            self.file_name = 'yolov7-object-detection.parquet'
            self.url = f"{BASE_URL}/Table?filePath={os.path.join(DATA_DIR, self.file_name)}"
            logger.info(f"Table URL: {self.url}")

    def test_bubble_plot(self):
        with playwright_page(headless=True) as page:
            # Navigate to the home page
            page.goto(self.url)
            page.wait_for_load_state('networkidle')
            pl = PageLocator(page)
            page.locator('button#btn-layout-side-by-side').click()
            pl.tab_panel_header('BubblePlot').click()
            pl.select_column('bubblePlotXColumn', 'confidence')
            pl.select_column('bubblePlotYColumn', 'iou')
            pl.select_column('galleryVisualColumn', 'bbox_viz')
            pl.select_column('galleryCaptionColumn', 'category_name')

            logger.info('Bubble plot is rendered')

            # Share
            page.locator('button[aria-label="SpeedDial"]').hover()
            share_button = page.locator('button[aria-label="Share"]')
            share_button.click()
            dialog = page.locator('div[role="dialog"]')
            dialog.wait_for(state='visible')
            share_link = dialog.locator('p:has-text("http://")').inner_text()
            self.assertTrue(share_link.endswith('.json'))

            logger.info(f"Share link: {share_link}")
            # Opening the shared link, you should see iframes.
            page.goto(share_link)
            page.wait_for_load_state('networkidle')
            iframe_count = page.locator('iframe').count()
            self.assertEqual(iframe_count, 10)








if __name__ == '__main__':
    unittest.main()


