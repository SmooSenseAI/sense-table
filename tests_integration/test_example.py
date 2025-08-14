import unittest

from my_logging import getLogger
from playwright.sync_api import expect
from playwright_utils import PlaywrightTestMixin, playwright_page

logger = getLogger(__name__)


class TestExample(unittest.TestCase, PlaywrightTestMixin):
    def test_apple_iphone_lineup(self):
        with playwright_page(headless=True) as page:
            # Step 1: Go to Apple homepage
            page.goto("https://www.apple.com")

            # Step 2: Click "iPhone" tab in the top nav
            page.locator('[data-globalnav-item-name="iphone"]').click()

            # Step 3: Expect URL to be correct
            expect(page).to_have_url("https://www.apple.com/iphone/")

            # Step 4: Scroll to "Explore the lineup"
            heading = page.get_by_role("heading", name="Explore the lineup")
            heading.scroll_into_view_if_needed()

            # Step 5: Expect 4 iPhone models below
            lineup_section = page.locator('section:has-text("Explore the lineup")')
            cards = lineup_section.locator(".product-tile")
            expect(cards).to_have_count(4)

            # Get product titles from each card
            titles = []
            for card in cards.all():
                title = card.locator(".product-tile-headline").inner_html()
                self.assertIn("iPhone", title)
                titles.append(title)

            logger.info(f"Found iPhone models: {titles}")

            # Use the mixin method to assert page title
            self.assert_page_title_contains(page, "iPhone")


if __name__ == "__main__":
    unittest.main()
