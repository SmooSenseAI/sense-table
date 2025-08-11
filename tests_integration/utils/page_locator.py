
import logging

logger = logging.getLogger(__name__)

class PageLocator:
    def __init__(self, page):
        self.page = page

    def locate_and_wait(self, selector: str, timeout=15000, scroll=False):
        self.page.wait_for_selector(selector, timeout=timeout)
        element = self.page.locator(selector).last
        if scroll:
            element.scroll_into_view_if_needed()
        return element

    def border_panel_header(self, name: str):
        return self.locate_and_wait(f"div.flexlayout__border_button:has-text('{name}')")

    def tab_panel_header(self, name: str):
        return self.locate_and_wait(f"div.flexlayout__tab_button:has-text('{name}')")

    def table_root(self):
        return self.locate_and_wait("div.ag-root-wrapper")

    def table_header(self, column: str):
        return self.locate_and_wait(f"span.ag-header-cell-text:text-is('{column}')")

    def table_header_sort_button(self, column: str):
        column_header = self.table_header(column)
        # Get the sibling column header
        # Get the parent element that contains the column header
        sort_button = column_header.locator("xpath=..").locator(f"[data-ref=eLabel]")
        return sort_button

    def column_stats_cell(self, column: str):
        return self.locate_and_wait(f"#column-stats-cell-{column}", scroll=True)

    def column_stats_card(self, column: str):
        return self.locate_and_wait(f"#column-stats-card-{column}", scroll=True)

    def column_cells(self, column: str):
        return self.page.locator(f"div.ag-cell[col-id='{column}']").all()

    def column_cell_values(self, column: str):
        values = [cell.inner_text() for cell in self.column_cells(column)]
        # Skip the header cell
        return values[1:]

    def column_navigation_button(self, column: str):
        return self.locate_and_wait(f"div.column-navigation-item:has-text('{column}')", scroll=True)

    def icon_color_mode(self):
        return self.locate_and_wait('#icon-button-color-mode')

    def select_column(self, settingKey, value):
        selector = self.page.locator(f'#select-column-{settingKey}')
        selector.click()
        selector.fill(value)
        self.page.locator(f"li[role='option'] >> text={value}").click()
        self.page.wait_for_load_state('networkidle')

    def folder_nav_item(self, name: str):
        return self.locate_and_wait(f"li.folder-nav-item:has-text('{name}')", scroll=True)

    def sql_status_count_running_0(self):
        return self.page.locator("#sql-status-count-running:has-text('0')")

    def get_relative_x_of_column(self, column: str):
        table = self.table_root()
        table.wait_for(state='visible')
        column_header = self.table_header(column)
        column_header.wait_for(state='visible')
        return column_header.bounding_box()['x'] - table.bounding_box()['x']
