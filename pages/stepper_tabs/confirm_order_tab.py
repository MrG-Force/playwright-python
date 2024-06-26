import re
from typing import Dict
from playwright.sync_api import Page, Locator

from pages.components.table import Table
from utils.text_utils import normalize_text


class ConfirmOrderTab:
    def __init__(self, page: Page):
        self.page = page
        self.order_details_section = self.get_section_by_header("Order Details")

    def get_section_by_header(self, header_text: str) -> Locator:
        header = self.page.locator("[role='button']").filter(has_text=header_text)
        self.expand_section_with_header(header_text)
        return self.page.locator("mat-expansion-panel").filter(has=header)

    def click_submit_order(self):
        active_tab = self.page.locator("[role='tabpanel'][aria-expanded='true']")
        active_tab.get_by_role("button", name="Submit Order").click()

    def get_order_total(self) -> Locator:
        active_tab = self.page.locator("[role='tabpanel'][aria-expanded='true']")
        return active_tab.get_by_text(re.compile(r"^\s*Total\s\d+(\.\d+)?$"))

    def expand_section_with_header(self, header_text: str):
        header = self.page.locator("[role='button']").filter(has_text=header_text)
        if header.get_attribute("aria-expanded") == "false":
            header.click()
        section_content_id = header.get_attribute("aria-controls")
        self.page.locator(f"#{section_content_id}").wait_for(state="visible")

    def collapse_section_with_header(self, header_text: str):
        header = self.page.locator("[role='button']").filter(has_text=header_text)
        if header.get_attribute("aria-expanded") == "true":
            header.click()

    def get_item_in_order_by_title(self, title: str) -> Dict[str, str]:
        table_element = self.order_details_section.locator("table").first
        table = Table(table_element)
        return table.get_row_as_dict_by_column_name_and_value("Item", title)

    def get_order_items(self) -> Dict[str, Dict[str, str]]:
        table_element = self.order_details_section.locator("table").first
        table = Table(table_element)
        return table.get_rows_as_dict("Item")

    def order_contains_items(self, items: list[Dict[str, str]]) -> bool:
        order_items_titles = self.get_order_items().keys()
        return all(item["title"] in order_items_titles for item in items)

    def get_contact_details(self) -> Dict[str, str]:
        order_details_section = self.get_section_by_header("Delivery & Contact Details")
        table_element = order_details_section.locator("table").first

        details = {}

        details["full_name"] = normalize_text(
            table_element.locator("xpath=.//tr[2]/td[4]").inner_text()
        )
        details["full_address"] = normalize_text(
            table_element.locator("xpath=.//tr[3]/td[4]").inner_text()
        )
        details["email"] = normalize_text(
            table_element.locator("xpath=.//tr[4]/td[3]").inner_text()
        )
        details["phone_number"] = normalize_text(
            table_element.locator("xpath=.//tr[5]/td[3]").inner_text()
        )
        return details

    def get_delivery_details(self) -> Dict[str, str]:
        order_details_section = self.get_section_by_header("Delivery & Contact Details")
        table_element = order_details_section.locator("table").first

        details = {}

        details["full_name"] = normalize_text(
            table_element.locator("xpath=.//tr[2]/td[2]").inner_text()
        )
        details["full_address"] = normalize_text(
            table_element.locator("xpath=.//tr[3]/td[2]").inner_text()
        )
        return details

    def get_payment_details(self) -> Dict[str, str]:
        order_details_section = self.get_section_by_header("Payment Details")
        table_element = order_details_section.locator("table").first

        details = {}

        details["name_on_card"] = normalize_text(
            table_element.locator("xpath=.//tr[1]/td[2]").inner_text()
        )
        details["card_number"] = normalize_text(
            table_element.locator("xpath=.//tr[2]/td[2]").inner_text()
        )
        details["card_type"] = normalize_text(
            table_element.locator("xpath=.//tr[3]/td[2]").inner_text()
        )
        details["expiry_date"] = normalize_text(
            table_element.locator("xpath=.//tr[4]/td[2]").inner_text()
        )
        details["cvv"] = normalize_text(
            table_element.locator("xpath=.//tr[5]/td[2]").inner_text()
        )
        return details
