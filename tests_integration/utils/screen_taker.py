import os
import pathlib

from utils.page_locator import PageLocator

PWD = os.path.dirname(os.path.abspath(__file__))


class ScreenTaker:
    def __init__(self, page, subfolder: str):
        self.page = page
        self.pl = PageLocator(page)
        self.screenshot_dir = os.path.join(PWD, "../../docs/public/images", subfolder)
        self.toggle = self.pl.icon_color_mode()
        pathlib.Path(self.screenshot_dir).mkdir(parents=True, exist_ok=True)

    def _take(self, component, name: str, pre_actions=None, post_actions=None):
        mode = self.toggle.get_attribute("data-mode")
        assert mode in ["light", "dark"]
        if pre_actions:
            pre_actions()
        component.screenshot(path=f"{self.screenshot_dir}/{name}_{mode}.jpg")
        if post_actions:
            post_actions()

    def take(self, component, name: str, pre_actions=None, post_actions=None):
        self._take(component, name, pre_actions, post_actions)

        self.toggle.click()
        self.page.wait_for_timeout(100)
        self._take(component, name, pre_actions, post_actions)
