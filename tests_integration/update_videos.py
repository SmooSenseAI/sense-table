import os
from my_logging import getLogger
from playwright_utils import BASE_URL, DATA_DIR, SCREEN_WIDTH, SCREEN_HEIGHT
from basetestcase import BaseTestCase, PageLocator, ScreenTaker
import unittest
import shutil
import pathlib
from contextlib import contextmanager
from playwright.sync_api import sync_playwright
import uuid
import time

logger = getLogger(__name__)
PWD = os.path.dirname(os.path.abspath(__file__))
VIDEO_BASE_DIR = os.path.join(PWD, '../docs/public/videos')

SCREENSHOT_DIR = os.path.join(PWD, '../docs/public/images/folder_browser')

@contextmanager
def playwright_page_with_video(file_rel_path: str, browser_type='chromium', **browser_options):
    with sync_playwright() as p:
        # Get the browser launcher based on type
        browser_launcher = getattr(p, browser_type)

        temp_dir = f'/tmp/{uuid.uuid4()}'
        pathlib.Path(temp_dir).mkdir(parents=True, exist_ok=True)
        # Launch browser with options
        browser = browser_launcher.launch(headless=False, **browser_options)
        try:
            context = browser.new_context(
                viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
                device_scale_factor=1,
                record_video_dir = temp_dir,
                record_video_size = {"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}
            )

            # Create new page
            page = context.new_page()
            logger.info(f"Browser launched ({browser_type}, video_dir={temp_dir})")

            yield page

        finally:
            # Always close browser, even if an exception occurs
            browser.close()
            logger.debug("Browser closed")
            time.sleep(1)  # Wait for video to be saved
            dest = os.path.join(VIDEO_BASE_DIR, file_rel_path)
            pathlib.Path(os.path.dirname(dest)).mkdir(parents=True, exist_ok=True)
            for f in os.listdir(temp_dir):
                if f.endswith('.webm'):
                    shutil.move(os.path.join(temp_dir, f), dest + '.webm')
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.debug(f"Video directory {temp_dir} deleted")


def take_themed_video(file_rel_path: str, url, actions):
    with playwright_page_with_video(file_rel_path=f'{file_rel_path}_dark') as page:
        page.goto(url)
        actions(page)
    with playwright_page_with_video(file_rel_path=f'{file_rel_path}_light') as page:
        page.goto(url)
        page.locator('#icon-button-color-mode').click()
        actions(page)


class UpdateVideos(BaseTestCase):

    def test_preview_images(self):
        url = f"{BASE_URL}/FolderBrowser?rootFolder=s3://sense-table-demo/datasets"
        def actions(page):
            pl = PageLocator(page)
            pl.folder_nav_item('Oxford Flowers 102').click()
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(1000)

        take_themed_video(file_rel_path='preview_images', url=url, actions=actions)


    def test_preview_csv_file(self):
        """Test that the folder browser can preview a csv file"""
        url = f"{BASE_URL}/FolderBrowser?rootFolder=s3://sense-table-demo/Preview Files"

        def actions(page):
            pl = PageLocator(page)
            pl.folder_nav_item('OpenVid-1M.csv').click()
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(1000)

        take_themed_video(file_rel_path='preview_csv', url=url, actions=actions)


    def test_preview_parquet_file(self):
        """Test that the folder browser can preview a csv file"""
        url = f"{BASE_URL}/FolderBrowser?rootFolder=s3://sense-table-demo/datasets"

        def actions(page):
            pl = PageLocator(page)
            pl.folder_nav_item('ClickBench-100M.parquet').click()
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(1000)

        take_themed_video(file_rel_path='preview_parquet', url=url, actions=actions)



if __name__ == '__main__':
    unittest.main()


